from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    path('logout/confirm/', views.LogoutConfirmView.as_view(), name='logout_confirm'),
    path('logout/', views.logout_view, name='logout'),

]

