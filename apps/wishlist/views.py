from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Wishlist, Item
from ..loginreg.models import User
from django.contrib import messages
# Create your views here.
def userinit(request):
    u = User.manager.get(id=request.session['id'])
    Wishlist.manager.create(user=u)
    return redirect(reverse('wishlist:index'))

def index(request):
    u = User.manager.get(id=request.session['id'])
    w = Wishlist.manager.get(user=u)
    i = Wishlist.manager.get_items(request.session['id'])
    context = {
        'me': u,
        'my_list': i,
        'other_items': Item.manager.get_items_not_in_wishlist(request.session['id'])
    }
    return render(request, 'wishlist/index.html', context)

def add(request):
    return render(request, 'wishlist/add.html')

def create(request):
    if not request.method=='POST':
        return redirect(reverse('wishlist:add'))

    i = Item.manager.new_item(request.POST)
    if i[0]:
        for s in i[1]:
            messages.success(request, s)
        return redirect(reverse('wishlist:index'))
    else:
        for e in i[1]:
            messages.error(request, e)
        return redirect(reverse('wishlist:add'))

def addtomylist(request, id):
    Wishlist.manager.add_item(id, request.session['id'])
    return redirect(reverse('wishlist:index'))

def item(request, id):
    i = Item.manager.filter(id=id)
    if not i:
        messages.error(request, 'Item does not exist!')
        return redirect(reverse('wishlist:index'))
    i = i[0]

    context = {
        'item': i,
        'wishlists': Item.manager.get_wishlists_containing_item(id)
    }
    return render(request, 'wishlist/item.html', context)

def remove(request, id):
    Wishlist.manager.remove_item(id, request.session['id'])
    return redirect(reverse('wishlist:index'))

def delete(request, id):
    result = Item.manager.delete_item(id, request.session['id'])
    if result[0]:
        for s in result[1]:
            messages.success(request, s)
    else:
        for e in i[1]:
            messages.error(request, e)

    return redirect(reverse('wishlist:index'))
