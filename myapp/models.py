from django.db import models
from django.contrib.auth.models import User

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

# New UserProfile model to extend User with additional fields
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Signal to automatically create a UserProfile whenever a User is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Job(models.Model):
    title = models.CharField(max_length=225)
    content=models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    created_at=models.DateField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title