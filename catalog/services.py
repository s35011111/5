from django.shortcuts import get_object_or_404
from .models import Product, Category


def get_products_by_category_id(category_id=None, active_only=True):
    products = Product.objects.all()
    if active_only:
        products = products.filter(published=True)
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    return products.select_related('category')


def get_products_by_category_name(category_name=None, active_only=True):
    products = Product.objects.all()
    if active_only:
        products = products.filter(published=True)
    if category_name:
        category = get_object_or_404(Category, name=category_name)
        products = products.filter(category=category)
    return products.select_related('category')

def get_all_categories():
    return Category.objects.all()

def get_categories_with_products():
    return Category.objects.filter(product__published=True).distinct()


