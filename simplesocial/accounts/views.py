from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
# Create your views here.
from .import forms
from django.views.generic import CreateView

class Signup(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = "accounts/signup.html"
