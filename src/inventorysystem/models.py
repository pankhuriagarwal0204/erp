from __future__ import unicode_literals
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
import uuid
from django.conf import settings
from simple_history.models import HistoricalRecords


class ItemType(models.Model):

    STATUS = (
        ("active", "active"),
        ("dead", "dead"),
        ("used", "used")
    )
    uuid = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default="active")
    total_quantity = models.IntegerField(default=0)
    total_issued_quantity = models.IntegerField(default=0, editable=False)
    in_stock_quantity = models.IntegerField(default=0, editable=False)

    issued_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    quantity_issued = models.IntegerField(default=0, null=True, blank=True)
    issued_on = models.DateTimeField(null=True, blank=True)
    returned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='returned_by')
    quantity_returned = models.IntegerField(default=0, null=True, blank=True)
    returned_on = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def assign(self):
        print "in assign"
        amount = self.quantity_issued
        items = self.item_set.all()
        for i in items:
            if amount>0 and i.available:
                i.available = False
                i.owner = self.issued_to
                amount = amount-1
                i.save()

    def create_items(self):

        items = self.item_set.count()

        if items == 0:
            for i in range(0, self.total_quantity):
                item_name = self.name + str(i+1)
                item_instance = Item(itemname=item_name)
                item_instance.save()
                self.item_set.add(item_instance)

    def rtrn(self):
        items = self.item_set.all()
        amount = self.quantity_returned

        print "in return %r" %amount

        for item in items:
            if amount>0 and not item.available:
                if item.owner == self.returned_by:
                    item.available = True
                    amount = amount - 1
                    item.owner = None
                    item.save()


    def clean(self):

        if self.issued_to or self.issued_on:
            if not self.issued_to:
                raise ValidationError({'issued_to': ('This field can not be blank')})
            elif not self.issued_on:
                raise ValidationError({'issued_on': ('Issual date can not be blank')})
            elif self.quantity_issued == 0:
                raise ValidationError({'quantity_issued': ('Quantity issued cannot be zero')})
            if self.quantity_issued > self.in_stock_quantity:
                raise ValidationError({'quantity_issued': ('Cannot issue: not enough stock')})

        if self.returned_on or self.returned_by:
            if not self.returned_by:
                raise ValidationError({'returned_by': ('This field can not be blank')})
            if self.quantity_returned == 0:
                raise ValidationError({'quantity_returned': ('Quantity returned cannot be zero')})
            if self.quantity_returned > self.quantity_issued:
                raise ValidationError({'quantity_returned': ('Quantity returned cannot be greater than quantity issued')})
            if self.issued_on > self.returned_on:
                raise ValidationError({'returned_on': ('Returned date cannot be before than issued date')})

        self.name = self.name.upper()

    def save(self, *args, **kwargs):

        self.create_items()
        try:
            previous_data = ItemType.objects.get(uuid=self.uuid)
            print previous_data.issued_to

            if previous_data.issued_on != self.issued_on:
                self.assign()

            if previous_data.returned_on != self.returned_on:
                print self.quantity_returned
                self.rtrn()
        except ObjectDoesNotExist:
            pass

        items = self.item_set.all()

        self.in_stock_quantity = 0

        for i in items:
            if i.available:
                self.in_stock_quantity = self.in_stock_quantity + 1

        self.total_issued_quantity = self.total_quantity - self.in_stock_quantity


        if(self.total_quantity == 0):
            self.status = "dead"
        elif(self.in_stock_quantity == 0):
            self.status = "used"
        else:
            self.status = "active"


        super(ItemType, self).save(*args, **kwargs)



class Item(models.Model):

    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    available = models.BooleanField(default=True)
    itemtype = models.ForeignKey(ItemType, null=True, blank=True, related_name='item_set')
    itemname = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def __str__(self):
        return self.itemname
