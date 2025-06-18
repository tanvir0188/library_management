from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()
  first_name = forms.CharField(max_length = 20)
  last_name = forms.CharField(max_length = 20)
  
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
  
  def save(self, commit=True):
    user = super().save(commit=False)
    user.email=self.cleaned_data.get('email')
    user.first_name=self.cleaned_data.get('first_name')
    user.last_name=self.cleaned_data.get('last_name')
    user.role=User.MEMBER
    if commit:
      user.save()
    return user