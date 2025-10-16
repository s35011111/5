from django.contrib import admin

# Register your models here.
from django.contrib import admin


from django.contrib import admin
from .models import  Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author',  'created_at', 'view_count', 'published']
    list_filter = [ 'created_at', 'published']
    search_fields = ['title', 'content']
    list_editable = ['published']

