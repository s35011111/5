from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product
def home_page(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'home.html', {'products': products})




def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product,}
    return render(request, 'product_detail.html', context)



def product_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'product_list.html', {'products': products})


def contacts(request):
    return render(request,'contacts.html')

