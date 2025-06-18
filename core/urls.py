from django.urls import path
from .views import general_login, logout, member_register, index


app_name='core'
urlpatterns = [
  path('login',general_login, name='login'),
  path('logout', logout, name='logout'),
  path('register', member_register, name='register'),
  path('index',index, name='index')
]

