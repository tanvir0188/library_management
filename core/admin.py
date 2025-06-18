from django.contrib import admin
from .models import User, Book, BookIssue, Profile
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# Register your models here.

class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('email', 'username', 'role')


class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = User
    fields = ('email', 'username', 'role', 'password')


class UserAdmin(BaseUserAdmin):
  add_form = CustomUserCreationForm
  form = CustomUserChangeForm
  model = User

  list_display = ('email', 'username', 'role', 'is_active')
  list_filter = ('role', 'is_active')

  fieldsets = (
    (None, {'fields': ('email', 'username', 'password')}),
    ('Permissions', {'fields': ('is_active', 'is_staff',
      'is_superuser', 'groups', 'user_permissions')}),
    ('Role', {'fields': ('role',)}),
  )

  add_fieldsets = (
    (None, {
      'classes': ('wide',),
      'fields': ('email', 'username','first_name', 'last_name', 'role', 'password1', 'password2', 'is_active')}
    ),
  )

  search_fields = ('email', 'username')
  ordering = ('email',)


class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author')


class BookIssueAdmin(admin.ModelAdmin):
  list_display = ('member', 'book', 'member', 'issued_by',
    'issue_date', 'due_date', 'is_returned', 'return_date')


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
