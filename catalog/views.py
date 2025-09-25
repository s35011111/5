from django.shortcuts import render,HttpResponse

# Create your views here.



def home(request):
    return render(request, 'home.html')


def contacts(request):
    return render(request,'contacts.html')

def catalog(request):
    pass

from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

