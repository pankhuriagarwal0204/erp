from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import views

urlpatterns = [
    url(r'^itemtypes/', views.ItemTypeList, name='itemtypelist'),
    url(r'^additem/', views.AddItemType, name='additem'),
    url(r'^items/(?P<id>[0-9a-f-]+)/', views.ItemList, name='itemlist'),
    url(r'^issueitem/', views.IssueItem.as_view(), name='issueitem'),
    url(r'^returnitem/', views.ReturnItem.as_view(), name='returnitem'),
    url(r'^fetchusers/(?P<id>[0-9a-f-]+)/$', views.ReturnItemUsers, name='fetchusers'),
    url(r'^add_department/', views.AddDepartment.as_view(), name='add_department'),
    url(r'^list_everything/$', views.aggregators, name='list_everything'),
]
