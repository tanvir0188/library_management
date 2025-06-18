from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User

def profile_created(sender, instance, created, **kwargs):
  if created:
    user = instance
    profile = Profile.objects.create(
      user = user,
      full_name = user.first_name+" "+user.last_name
    )
  
post_save.connect(profile_created, sender=User)