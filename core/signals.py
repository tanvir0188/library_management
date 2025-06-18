from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book, BookIssue, Profile, User

def profile_created(sender, instance, created, **kwargs):
  if created:
    user = instance
    profile = Profile.objects.create(
      user = user,
      full_name = user.first_name+" "+user.last_name
    )
  
post_save.connect(profile_created, sender=User)


@receiver(post_save, sender=BookIssue)
def issue_created(sender, instance, created, **kwargs):
  if created and instance.book:
    book = instance.book
    book.available_copies = max(0, book.available_copies - 1)  # avoid negative copies
    book.save()