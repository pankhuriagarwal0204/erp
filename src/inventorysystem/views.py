from braces.views import SuperuserRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from braces.views import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect, response
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.generic import ListView, View
import models
import inventoryforms

@login_required
@user_passes_test(lambda u: u.is_superuser)
def ItemTypeList(request):
    itemtypes = models.ItemType.objects.all()
    context = {
        'itemtypes' : itemtypes
    }
    return TemplateResponse(request, 'inventorysystem/display_list.html', context)



@login_required
@user_passes_test(lambda u: u.is_superuser)
def aggregators(request):
    department = models.Department.objects.all()
    item_types = models.ItemType.objects.all()
    items = models.Item.objects.all()
    # requested_items = Requested_Items.objects.all()
    context = {
        'department': department,
        'item_type': item_types,
        'item': items,
    }
    return TemplateResponse(request, 'list_view.html', context)
	# if request.method == 'GET':
	# 	if request.user.is_authenticated:
	# 		if request.user.is_superuser:
	#
	# 	# 	elif request.user.groups.values_list('name', flat=True).exists():
	# 	# 		requested_items = Requested_Items.objects.filter(owner=request.user)
	# 	# 		context = {
	# 	# 			'requested':requested_items,
	# 	# 		}
	# 	# 		return TemplateResponse(request, 'list_view.html', context)
	# else:
	# 	return redirect(reverse('login'))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def AddItemType(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            form = inventoryforms.AddItemForm()
            return TemplateResponse(request, 'inventorysystem/additem.html', {'form' : form})
        else:
            raise PermissionDenied

    elif request.method == 'POST':
        form = inventoryforms.AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/api/itemtypes/')
        else:
            print form.errors
            return TemplateResponse(request, 'inventorysystem/additem.html', {'form': form})
    else:
        raise PermissionDenied


class AddDepartment(SuperuserRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form = inventoryforms.AddDepartmentForm()
        return TemplateResponse(request, 'inventorysystem/additem.html', {'form' : form})

    def post(self, request, *args, **kwargs):
        form = inventoryforms.AddDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/api/itemtypes/')
        else:
            print form.errors
            return TemplateResponse(request, 'inventorysystem/additem.html', {'form': form})

@login_required
def ItemList(request, id):
    print id
    itemtype = models.ItemType.objects.get(uuid = id)
    items = itemtype.item_set.all()
    context = {
        'items' : items
    }
    return TemplateResponse(request, 'inventorysystem/items_list.html', context)

class IssueItem(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        form = inventoryforms.IssueItemForm()
        return TemplateResponse(request, 'inventorysystem/additem.html', {'form': form})

    def post(self, request, *args, **kwargs):

        form = inventoryforms.IssueItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/api/itemtypes/')
        else:
            print form.data
            return TemplateResponse(request, 'inventorysystem/additem.html', {'form': form})

class ReturnItem(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = inventoryforms.ReturnItemForm()
        return TemplateResponse(request, 'inventorysystem/returnitem.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = inventoryforms.ReturnItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/api/itemtypes/')
        else:
            print form.data
            return TemplateResponse(request, 'inventorysystem/returnitem.html', {'form': form})

@login_required
def ReturnItemUsers(request, id):
    item_instance = models.ItemType.objects.get(uuid = id)
    items = item_instance.item_set.all()
    def extract_users(item):
        return str(item.owner) + ","

    users = list(map(extract_users, items))

    print users

    data = {
        'items' : users
    }
    return HttpResponse(users)