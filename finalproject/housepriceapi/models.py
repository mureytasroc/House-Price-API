from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=30)
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "User[username: " + self.user.username + ", name: " + self.name \
               + ", email: " + self.email + ", api_key: " + self.api_key + "]"

    def __lt__(self, other):
        return self.updated_at < other.updated_at

    def __gt__(self, other):
        return self.updated_at > other.updated_at

    def __le__(self, other):
        return self.updated_at <= other.updated_at

    def __ge__(self, other):
        return self.updated_at >= other.updated_at


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
