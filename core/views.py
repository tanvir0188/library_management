from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Book, Profile, User, BookIssue
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from .forms import BookForm, BookIssueForm, ProfileForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
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
      messages.success(request,f'Welcome, {request.user.username}')
      return redirect('core:index')
    else:
      messages.info(request, f'Account name does not exist, Please signup')
  
  form = AuthenticationForm()
  context={
    'form':form
  }
  return render(request, 'login.html', context)

class AdminNotAllowed:
  def dispatch(self, request, *args, **kwargs):
    if(request.user.role==0):
      messages.error(request,f'Admin cant login here')
      return redirect('core:login')
    return super().dispatch(request, *args, **kwargs)
  
class BookListView(LoginRequiredMixin,AdminNotAllowed, ListView):
  model = Book
  paginate_by = 10
  template_name='index.html'
  ordering = ['created_at']
  login_url='core:login'

class ProfileUpdateView(LoginRequiredMixin, AdminNotAllowed, UpdateView):
  model = Profile
  form_class = ProfileForm
  template_name = 'profile.html'
  login_url='core:login'

  def get_object(self, queryset=None):
    return Profile.objects.get(user__username=self.kwargs['username'])
  
  def get_success_url(self):
    return reverse_lazy('core:profile-update', kwargs={'username': self.request.user.username})

#if we use the generic view only
# class ProfileUpdateView(LoginRequiredMixin, AdminNotAllowed, UpdateView):
#   model = Profile
#   fields = ['image', 'full_name', 'address']
#   template_name = 'profile.html'
#   def get_object(self, queryset=None):
#     return get_object_or_404(Profile, user__username=self.kwargs['username'])

#   def get_success_url(self):
#     return reverse_lazy('profile', kwargs={'username': self.request.user.username})

class BookCreateView(LoginRequiredMixin, AdminNotAllowed, CreateView):
  model = Book
  form_class = BookForm
  template_name = 'book.html'
  login_url='core:login'
  
  def get_success_url(self):
    messages.success(self.request, f'Successfully added the new book')
    return reverse_lazy('core:index')

class BookIssueCreateView(LoginRequiredMixin, AdminNotAllowed, CreateView):
  model = BookIssue
  form_class = BookIssueForm
  template_name = 'book-issue.html'
  login_url = 'core:login'

  def form_valid(self, form):
    form.instance.issued_by = self.request.user
    messages.success(self.request, f'Successfully issued to {form.instance.member.username}')
    return super().form_valid(form)
  

  def get_success_url(self):
    
    return reverse_lazy('core:index')
  
class BookIssueListView(LoginRequiredMixin, AdminNotAllowed, ListView):
  model = BookIssue
  paginate_by = 10
  template_name='issue-list.html'
  ordering = ['return_date']
  login_url='core:login'  






