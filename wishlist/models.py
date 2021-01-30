from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import uuid

from products.models import Product
from profiles.models import UserProfile


class Wishlist(models.Model):
    wishlist_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, blank=False, related_name='wishlist', default=1)
    item_count = models.IntegerField(null=True, blank=False)

    def _generate_wishlist_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_count(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.item_count = WishLineItem.objects.filter(wishlist=self).count()
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.wishlist_number:
            self.wishlist_number = self._generate_wishlist_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Wishlist {self.id} for user {self.user_profile.user}'


class WishLineItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, null=False, blank=False, on_delete=models.CASCADE, related_name='wishitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    wishitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the wishitem total
        and update the order total.
        """
        if self.product.sale is True:
            self.wishitem_total = self.product.saleprice * self.quantity
        else:
            self.wishitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on wishlist {self.wishlist.id}'


@receiver(post_save, sender=WishLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.wishlist.update_count()


@receiver(post_delete, sender=WishLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.wishlist.update_count()
