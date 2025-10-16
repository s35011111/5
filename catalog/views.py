from itertools import product

from django.core.exceptions import PermissionDenied
from django.views.generic import  TemplateView

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product
from .forms import ProductForm, ProductModeratorForm


class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    def get_queryset(self):
        return Product.objects.filter(published=True)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    def get_queryset(self):
        return Product.objects.filter(published=True)

class ContactsView(TemplateView):
    model = Product
    template_name = 'contacts.html'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Product submitted for moderation')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_form.html'
    success_url = reverse_lazy('product_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        self.object = self.get_object()
        if request.user == self.object.owner:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()

    def get_form_class(self):
        if self.request.user.is_staff:
            return ProductModeratorForm
        return ProductForm



class ProductDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product=self.get_object()
        return self.request.user==product.owner

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ProductManagementView(ListView):
    model = Product
    template_name = 'product_management.html'
    context_object_name = 'products'
