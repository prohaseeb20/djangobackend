from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer,LoginSerializer, UserProfileSerializer,UserSerializer,JobSerializer
from .permissions import HasRole
from .models import Application, Job, UserProfile

class RegisterView(generics.CreateAPIView):
    queryset= User.objects.all()
    permission_classes=(AllowAny,)
    serializer_class= RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer    

    def post(self, request,*args, **kwargs):
        username= request.data.get('username')
        password= request.data.get('password')
        user = authenticate(username=username,password=password)

        if user is not None:  #important (generated)
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data

            })
        else:
            return Response({'detail':'Invalid credentials'},status=401)
        
class DashboardView(APIView):
    permission_classes= [IsAuthenticated,HasRole]
    required_role = 'teacher'   
    def get(self, request):
        user = request.user
        print('here is the user', user)
        user_serializer=UserSerializer(user)
        return Response({
        'message': 'Welcome to dashboard',
        'user': user_serializer.data
    
    }, 200)        



class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class= JobSerializer
    permission_classes= [IsAuthenticated]


    def perform_create(self,serializer):
        serializer.save(author=self.request.user)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset= Job.objects.all()
    serializer_class= JobSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(author=self.request.user)
        
class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class AppliedJobsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return jobs that the authenticated user has applied to
        return Job.objects.filter(applications__user=self.request.user)

    def get(self, request, *args, **kwargs):
        jobs = self.get_queryset()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
class ApplicantsForJobView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the job ID from the URL
        job_id = self.kwargs['job_id']
        job = get_object_or_404(Job, id=job_id)
        # Return users who have applied to the specific job
        return job.applications.all()

    def get(self, request, job_id, *args, **kwargs):
        applications = self.get_queryset()
        users = [app.user for app in applications]
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data)


class ApplyForJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        # Get the job the user is applying for
        job = get_object_or_404(Job, id=job_id)

        # Check if the user has already applied for this job
        if Application.objects.filter(user=request.user, job=job).exists():
            raise ValidationError("You have already applied for this job.")

        # Create a new application
        application = Application.objects.create(user=request.user, job=job)
        
        return Response(
            {"message": f"Successfully applied for {job.title}."},
            status=201
        )