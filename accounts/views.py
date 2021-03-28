from django.shortcuts import render
from django.contrib import auth, messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import RedirectView, CreateView
# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class LogoutView(RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, "You have successfully logged out")
        return super(LogoutView, self).get(request, *args, **kwargs)