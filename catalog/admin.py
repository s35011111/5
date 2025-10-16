from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Category, Product


# admin.site.register(Category)
# admin.site.register(Product)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category','owner','published']
    list_filter = ['category','published','owner']
    search_fields = ['name', 'description']
    autocomplete_fields = ['category']
    list_editable = ['price','published']
    actions = ['publish_products','unpublish_products']
    list_per_page = 20
    ordering = ['name']


