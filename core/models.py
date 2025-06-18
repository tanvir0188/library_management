from asyncio.windows_events import NULL
from django.utils import timezone 
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
  ADMIN=0
  LIBRARIAN=1
  MEMBER=2
  USER_LEVEL_CHOICES=(
    (ADMIN, "Admin"),
    (LIBRARIAN, "Librarian"),
    (MEMBER,"Member")
  )
  email = models.EmailField(unique=True)
  role = models.IntegerField(choices=USER_LEVEL_CHOICES, blank=True, default=MEMBER)

  USERNAME_FIELD='email'
  REQUIRED_FIELDS=['username']
  
  def __str__(self):
    return self.username
  def save(self, *args, **kwargs):
    if self.is_staff and self.role !=0:
      self.role = 0
    super().save(*args, **kwargs)

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  full_name =  models.CharField(max_length=255, null=True, blank=True)
  image = models.ImageField(blank=True, null=True, upload_to='uploads/profile')
  address = models.CharField(null=True, blank=True, max_length=255)
  
  def __str__(self):
    if self.full_name:
      return self.full_name
    return self.user.username 
  
  

class Book(models.Model):
  title = models.CharField(max_length=255, blank=False)
  author = models.CharField(max_length=200, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  total_copies=models.IntegerField(default=1, blank=True)
  available_copies = models.IntegerField(default=0, blank=True)

  def __str__(self):
    return self.title
  def save(self, *args, **kwargs):
    if self._state.adding and (self.available_copies==0):
      self.available_copies = self.total_copies
    super().save(*args, **kwargs)
      
  
class BookIssue(models.Model):
  member = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='book_issue_member',  limit_choices_to={'role': '2'})
  book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
  issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='book_issue_librarian')
  issue_date = models.DateField(blank=False, auto_now_add=True)
  due_date = models.DateField(blank=False, auto_now_add=False)
  return_date = models.DateField(null=True)
  is_returned = models.BooleanField(default=False)

  def __str__(self):
    return f'{self.member.username} - {self.book.title}'
  
  def save(self, *args, **kwargs):
    if self.is_returned == True and self.return_date is None:
      self.return_date = timezone.now().date()
    super().save(*args, **kwargs)
  

  
