from django.urls import path
from .views import BookCreateView, BookIssueCreateView, BookIssueListView, general_login, logout, member_register, BookListView, ProfileUpdateView


app_name='core'
urlpatterns = [
  path('login',general_login, name='login'),
  path('logout', logout, name='logout'),
  path('register', member_register, name='register'),
  path('index', BookListView.as_view(), name='index'),
  path('profile/<str:username>', ProfileUpdateView.as_view(), name='profile-update'),
  path('add-book', BookCreateView.as_view(), name='add-book'),
  path('issue-book', BookIssueCreateView.as_view(), name='issue-book'),
  path('issue-list', BookIssueListView.as_view(),name='issue-list')
]

