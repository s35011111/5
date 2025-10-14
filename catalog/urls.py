from django.conf.urls.static import static
from django.urls import path

from config import settings
from . import views

from django.urls import path
from . import views

# For function-based views
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('product_list/', views.ProductListView.as_view(), name='product_list'),
    path('product_list/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product_management/', views.ProductManagementView.as_view(), name='product_management'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)







