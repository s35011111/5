
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
########################################################################
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self: Any) -> str:
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

########################################################################
class Product(models.Model):
    name = models.CharField(max_length=100)
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    description = models.TextField()
    image=models.ImageField(upload_to='products/')
    price =models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self: Any) -> str:
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def clean(self):
        errors = {}
        if self._contains_prohibited_words(self.name):
            errors['name'] = 'Product name contains prohibited words.'
        if self._contains_prohibited_words(self.description):
            errors['description'] = 'Description contains prohibited words.'
        if self.price <= 0:
            errors['price'] = 'Price must be positive.'
        if errors:
            raise ValidationError(errors)


    def _contains_prohibited_words(self, text):
        prohibited_words = ["казино",    "криптовалюта",    "крипта",    "биржа",    "дешево",
        "бесплатно",    "обман",    "полиция",    "радар"]
        text_lower = text.lower()
        return any(prohibited_word in text_lower for prohibited_word in prohibited_words)


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



########################################################################
