from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^userinit$', views.userinit, name='userinit'),
    url(r'^item/add$', views.add, name='add'),
    url(r'^item/create$', views.create, name='create'),
    url(r'^item/addtomylist/(?P<id>\d+)$', views.addtomylist, name='addtomylist'),
    url(r'^item/(?P<id>\d+)$', views.item, name='item'),
    url(r'^item/remove/(?P<id>\d+)$', views.remove, name='remove'),
    url(r'^item/delete/(?P<id>\d+)$', views.delete, name='delete')
]
