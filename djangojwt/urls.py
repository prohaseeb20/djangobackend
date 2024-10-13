from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from myapp.views import RegisterView,LoginView,DashboardView, JobListCreateView,JobDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/',RegisterView.as_view(),name="auth_register"),
    path('api/auth/login/',LoginView.as_view(),name="auth_login"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', DashboardView.as_view(),name="dashboard"),
    path('api/jobs/', JobListCreateView.as_view() , name="job_list_create"),
    path('api/jobs/<int:pk>', JobDetailView.as_view() , name="job_detail"),
    ]
    

