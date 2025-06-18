from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Book, User, BookIssue
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def member_register(request):
  if request.method=='POST':
    form = UserRegisterForm(request.POST)

    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request,f'Your account has been created with the username {username}')
      return redirect('core:login')
  else:
    form =UserRegisterForm()
  
  context = {
    'form':form,
  }
  return render(request, 'register.html', context)

def general_login(request):
  if request.user.is_authenticated and request.user.role !=0:
    return redirect('core:index')
  
  
  if request.method=='POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None and user.role !=0:
      form=login(request,user)
      messages.success(request,f'Welcome, {username}')
      return redirect('core:index')
    else:
      messages.info(request, f'Account name does not exist, Please signup')
  
  form = AuthenticationForm()
  context={
    'form':form
  }
  return render(request, 'login.html', context)

@login_required
def index(request):  
  if request.user.role==0:
    return redirect('core:login')
  return render(request, 'index.html')


