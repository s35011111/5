from django.conf.urls.static import static
from django.urls import path

from config import settings
from . import views
"""
urlpatterns = [
    path('products/', views.product_list, name='product_list'),
]
"""
from django.urls import path
from . import views

# For function-based views
urlpatterns = [
    path('', views.home_page, name='home'),
    path('productslist/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('contacts/', views.contacts, name='contacts'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)







