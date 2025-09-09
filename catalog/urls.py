from django.urls import path
from . import views

#from config.urls import urlpatterns

urlpatterns=[path('', views.home, name='home'),path('home/', views.home, name='home'),path('contacts/', views.contacts, name='contacts'), ]
