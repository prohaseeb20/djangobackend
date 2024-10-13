from django.contrib import admin
from myapp.models import Role ,UserRole, UserProfile, Job

admin.site.register(Role)
admin.site.register(Job)
admin.site.register(UserRole)
admin.site.register(UserProfile)

