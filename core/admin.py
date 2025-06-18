from django.contrib import admin
from .models import User, Book, BookIssue, Profile
from django.utils.html import format_html
# Register your models here.
class UserAdmin(admin.ModelAdmin):
  list_display = ('username', 'email', 'role')
class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author')

class BookIssueAdmin(admin.ModelAdmin):
  list_display = ('member', 'book', 'member','issued_by', 'issue_date', 'due_date', 'is_returned', 'return_date')

class ProfileAdmin(admin.ModelAdmin):
  list_display = ('image_tag', 'full_name', 'user', 'address')
  def image_tag(sef, obj):
    if obj.image:
      return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;"/>', obj.image.url)
    return "No image"
  image_tag.short_description = 'Profile Image'

  
admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookIssue, BookIssueAdmin)
admin.site.register(Profile, ProfileAdmin)
