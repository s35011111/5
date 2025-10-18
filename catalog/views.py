from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic import TemplateView

from .forms import ProductForm, ProductModeratorForm
from .models import Product
from .services import get_products_by_category_id, get_categories_with_products


class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    def get_queryset(self):
        return Product.objects.filter(published=True)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    #context_object_name = 'products'

    @method_decorator(cache_page(60 * 30))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        if not settings.CACHE_ENABLED:
            return self.fetch_products_from_db()

        cache_key = self.get_cache_key()
        products = cache.get(cache_key)

        if products is None:
            products = self.fetch_products_from_db()
            cache.set(cache_key, products, 60 * 15)

        return products

    def get_cache_key(self):
        page = self.request.GET.get('page', '1')
        user_type = 'moderator' if self.request.user.has_perm('catalog.change_product') else 'public'
        return f"products_{user_type}_page_{page}"

    def fetch_products_from_db(self):

        if self.request.user.has_perm('catalog.change_product'):
            return Product.objects.all().select_related('owner').order_by('-created_at')
        else:
            return Product.objects.filter(published=True).select_related('owner').order_by('-created_at')



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


def product_list_by_id(request, category_id=None):
    products = get_products_by_category_id(category_id)
    categories = get_categories_with_products()
    context = {'products': products,'categories': categories,'current_category_id': category_id,}
    return render(request, 'product_filtered.html', context)

################################################################################








