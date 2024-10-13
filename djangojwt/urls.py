from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from myapp.views import ApplicantsForJobView, AppliedJobsView, ApplyForJobView, RegisterView,LoginView,DashboardView, JobListCreateView,JobDetailView, UserProfileDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/',RegisterView.as_view(),name="auth_register"),
    path('api/auth/login/',LoginView.as_view(),name="auth_login"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', DashboardView.as_view(),name="dashboard"),
    path('api/jobs/', JobListCreateView.as_view() , name="job_list_create"),
    path('api/jobs/<int:pk>', JobDetailView.as_view() , name="job_detail"),
    path('api/profile/', UserProfileDetailView.as_view(), name='user_profile'),
    path('api/jobs/applied/', AppliedJobsView.as_view(), name='applied_jobs'),
    path('api/jobs/<int:job_id>/applicants/', ApplicantsForJobView.as_view(), name='applicants_for_job'),
    path('api/jobs/<int:job_id>/apply/', ApplyForJobView.as_view(), name='apply_for_job'),
    ]
    

