from django import forms
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.utils import timezone

import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AddItemForm(forms.ModelForm):
    class Meta:
        model = models.ItemType
        fields = ['name', 'total_quantity']


class IssueItemForm(forms.ModelForm):

    item = forms.ModelChoiceField(widget=forms.Select, queryset=models.ItemType.objects.filter(in_stock_quantity__gt = 0).order_by('name'))

    user = forms.ModelChoiceField(widget=forms.Select, queryset=User.objects.all().order_by('name'))
    #issue_timestamp = forms.DateTimeField(widget = widgets.AdminSplitDateTime())

    class Meta:
        model = models.ItemType
        fields = ['item','quantity_issued', 'user']
        #widgets = {'issue_timestamp': widgets.AdminSplitDateTime()}

    def clean_quantity_issued(self):
        if self.cleaned_data['quantity_issued'] == 0:
            raise ValidationError('Quantity issued can not be 0.')
        item = self.data['item']
        print item
        item_instance = models.ItemType.objects.get(uuid=item)
        in_stock_quantity = item_instance.in_stock_quantity
        if in_stock_quantity < self.cleaned_data['quantity_issued']:
            raise ValidationError('Not enough Stock')
        return self.cleaned_data['quantity_issued']

    def save(self, commit=True):
        item = self.cleaned_data['item']
        print "item %r" %item
        item_instance = models.ItemType.objects.get(uuid = item)
        user_instance = User.objects.get(pk = self.cleaned_data['user'])
        item_instance.issued_to = user_instance
        item_instance.quantity_issued = self.cleaned_data['quantity_issued']
        item_instance.issued_on = timezone.now()
        item_instance.save()

class ReturnItemForm(forms.ModelForm):
    items = models.ItemType.objects.all()
    users = User.objects.all().order_by('name')

    item = forms.ModelChoiceField(widget=forms.Select, queryset=models.ItemType.objects.filter(total_issued_quantity__gt = 0))

    USERS = (('', '----------'),)
    for user in users:
        name = str(user.name)
        USERS = USERS + ((user.pk, name),)

    user = forms.ModelChoiceField(widget=forms.Select, queryset=User.objects.all().order_by('name'))

    class Meta:
        model = models.ItemType
        fields = ['item', 'user', 'quantity_returned']

    def clean_quantity_returned(self):
        if self.cleaned_data['quantity_returned'] == 0:
            raise ValidationError('Quantity returned cannot be 0.')
        item = self.data['item']
        print item
        item_instance = models.ItemType.objects.get(uuid=item)
        user = self.data['user']
        user_instance = User.objects.get(pk = user)
        items = item_instance.item_set.all()
        issued_amount = 0
        for i in items:
            if not i.available:
                if i.owner == user_instance:
                    issued_amount = issued_amount+1
        if issued_amount < self.cleaned_data['quantity_returned']:
            raise ValidationError('Quantity returned is greater than quantity issued')

    def save(self, commit=True):
        item = self.cleaned_data['item']
        item_instance = models.ItemType.objects.get(uuid = item)
        user_instance = User.objects.get(pk = self.cleaned_data['user'])
        item_instance.returned_by = user_instance
        #print self.data['quantity_returned']
        item_instance.quantity_returned = int(self.data['quantity_returned'])
        item_instance.returned_on = timezone.now()
        #print item_instance.returned_on
        item_instance.save()

