from django.core.mail import send_mail
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import DetailView,TemplateView,UpdateView
from django.contrib import messages
from django.contrib.auth import logout,login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserUpdateForm

User = get_user_model()

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'
    def get_object(self):
        return self.request.user

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            send_mail('Добро пожаловать!',f'{user.username} вы зарегистрированы','noreply@gmail.com',[user.email])
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('users:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'users/profile_form.html'
    success_url = '/users/profile/'
    def get_object(self):
        return self.request.user

class LogoutConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'users/logout_confirm.html'
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/users/logout/confirm/')




