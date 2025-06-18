from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from .models import Book, User, BookIssue
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
# Create your views here.

class SignUpView(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("login")
  template_name = "registration/signup.html"

def index(request):
  return render(request, 'register.html')