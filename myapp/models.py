from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Role model remains unchanged
class Role(models.Model):
   name = models.CharField(max_length=200, unique=True)

   def __str__(self):
       return self.name

# UserRole model remains unchanged
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

# UserProfile model to extend User with additional fields
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    roll_no = models.CharField(max_length=20, unique=True, null=True)  # Assuming roll number should be unique
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Signal to automatically create a UserProfile whenever a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)  # Nullable
    company = models.CharField(max_length=225, blank=True, null=True)  # Nullable
    designation = models.CharField(max_length=225, blank=True, null=True)  # Nullable
    content = models.TextField(blank=True, null=True)  # Nullable
    cgpa_cutoff = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)  # Nullable
    branches = models.CharField(max_length=255, blank=True, null=True)  # Nullable
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs', blank=True, null=True)  # Nullable
    created_at = models.DateField(auto_now_add=True)  # Automatically set, usually not nullable
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set, usually not nullable

    def __str__(self):
        return self.title

    

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')  # Prevent duplicate applications for the same job

    def __str__(self):
        return f"{self.user.username} applied for {self.job.title} on {self.applied_at}"
