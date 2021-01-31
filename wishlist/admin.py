from django.contrib import admin
from .models import Wishlist, WishLineItem


class WishLineItemAdminInline(admin.TabularInline):
    model = WishLineItem
    readonly_fields = ('wishitem_total',)


class WishlistAdmin(admin.ModelAdmin):
    inlines = (WishLineItemAdminInline,)

    readonly_fields = ('wishlist_number', 'item_count')

    fields = ('user_profile', 'item_count', 'wishlist_number')

    list_display = ('wishlist_number', 'user_profile', 'item_count')


admin.site.register(Wishlist, WishlistAdmin)
