from django.shortcuts import render,HttpResponse

# Create your views here.



def home(request):
    return render(request, 'home.html')


def contacts(request):
    return render(request,'contacts.html')

def catalog(request):
    pass
