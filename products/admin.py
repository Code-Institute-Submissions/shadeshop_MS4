from django.contrib import admin
from .models import Product, Brand, Review

# Register your models here.


class ReviewAdminInline(admin.TabularInline):
    model = Review


class ProductAdmin(admin.ModelAdmin):
    inlines = (ReviewAdminInline,)

    list_display = (
        'sku',
        'name',
        'brand',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
