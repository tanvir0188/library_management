from django.contrib import admin
from .models import User, Book, BookIssue
# Register your models here.
class UserAdmin(admin.ModelAdmin):
  list_display = ('username', 'email', 'role')
class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author')

class BookIssueAdmin(admin.ModelAdmin):
  list_display = ('member', 'book', 'member','issued_by', 'issue_date', 'due_date', 'is_returned', 'return_date')

admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookIssue, BookIssueAdmin)