from django import forms
from .models import Book, BookIssue, Profile, User
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
  
class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['image', 'full_name', 'address']
    widgets = {
      'image': forms.ClearableFileInput(
        attrs={
          'class': 'form-control'          
        } 
      ),
      'full_name':forms.TextInput(attrs={
        'class':'form-control'
      }),
      'address': forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Enter your address'
      })
    }
  def save(self, user=None, *args, **kwargs):
    profile = super().save(commit=False)
    profile.user = user or profile.user
    profile.save()
    return profile

class BookForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = ['title', 'author', 'total_copies', 'available_copies']
    widgets = {
      'title': forms.TextInput(attrs={
        'class':'form-control',        
      }),
      'author': forms.TextInput(attrs={
        'class': 'form-control'
      }),
      'total_copies':forms.NumberInput(attrs={
        'class':'form-control'
      }),
      'available_copies':forms.NumberInput(attrs={
        'class':'form-control'
      })
    }

class BookIssueForm(forms.ModelForm):
  class Meta:
    model = BookIssue
    fields = ['member','book', 'due_date']
    widgets = {
      'member':forms.Select(attrs={
        'class':'form-control'
      }),
      'book':forms.Select(attrs={
        'class':'form-control'
      }),

      'due_date': forms.DateInput(attrs={
      'class': 'form-control',
      'type': 'date'
    }),
    }
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['book'].empty_label = 'Choose book'
    self.fields['member'].empty_label = 'Choose a member'

