from __future__ import unicode_literals

from django.db import models
from ..loginreg.models import User
# Create your models here.

class ItemManager(models.Manager):
    def new_item(self, form_data):
        errors = []
        if not form_data['name']:
            errors.append('Item/Product name cannot be empty!')
        elif len(form_data['name']) < 3:
            errors.append('Item/Product name must be at least three characters!')
        if errors:
            return (False, errors)
        u = User.manager.get(id=form_data['id'])
        i = self.create(name=form_data['name'], added_by=u)
        w = Wishlist.manager.get(user=u)
        w.items.add(i)
        w.save()
        return (True, i)

    def get_items_not_in_wishlist(self, user_id):
        u = User.manager.get(id=user_id)
        w = Wishlist.manager.get(user=u)
        items = self.exclude(wishlists=w)
        return items

    def delete_item(self, item_id, user_id):
        errors = []
        i = self.get(id=item_id)
        u = User.manager.get(id=user_id)
        if i.added_by != u:
            errors.append('Not your item to delete!')
        if errors:
            return (False, errors)

        i.delete()
        return (True, ['Successfully deleted!'])

    def get_wishlists_containing_item(self, item_id):
        i = self.get(id=item_id)
        return [val for val in Wishlist.manager.all() if val in i.wishlists.all()]

class Item(models.Model):
    name = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name='my_items')
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    manager = ItemManager()

class WishlistManager(models.Manager):
    def get_items(self, user_id):
        u = User.manager.get(id=user_id)
        w = self.get(user=u)
        return [val for val in Item.manager.all() if val in w.items.all()]
    def add_item(self, item_id, user_id):
        i = Item.manager.get(id=item_id)
        u = User.manager.get(id=user_id)
        w = self.get(user=u)
        w.items.add(i)
        return True
    def remove_item(self, item_id, user_id):
        i = Item.manager.get(id=item_id)
        u = User.manager.get(id=user_id)
        w = self.get(user=u)
        w.items.remove(i)
        return True

class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='list')
    items = models.ManyToManyField(Item, related_name='wishlists', blank=True)
    manager = WishlistManager()
