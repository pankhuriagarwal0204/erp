from django.http import HttpResponse
from django.http import HttpResponseRedirect, response
from django.http import JsonResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic import ListView, View
import models
import inventoryforms


class ItemTypeList(View):
    def get(self,request, *args, **kwargs):
        itemtypes = models.ItemType.objects.all()
        context = {
            'itemtypes' : itemtypes
        }
        return TemplateResponse(request, 'inventorysystem/display_list.html', context)


class AddItemType(View):
    def get(self, request, *args, **kwargs):
        form = inventoryforms.AddItemForm()
        return TemplateResponse(request, 'inventorysystem/additem.html', {'form' : form})

    def post(self, request, *args, **kwargs):
        form = inventoryforms.AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/api/itemtypes/')
        else:
            print form.errors
            return TemplateResponse(request, 'inventorysystem/additem.html', {'form': form})

def ItemList(request, id):
    print id
    itemtype = models.ItemType.objects.get(uuid = id)
    items = itemtype.item_set.all()
    context = {
        'items' : items
    }
    return TemplateResponse(request, 'inventorysystem/items_list.html', context)

class IssueItem(View):
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

class ReturnItem(View):
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