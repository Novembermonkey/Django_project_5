from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Subject, Course, Comment
from .paginations import MyPagination
from .permissions import *
from .serializers import SubjectSerializer, CourseSerializer, CommentSerializer, RegisterSerializer, LoginSerializer, \
    CustomTokenObtainSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.functions import Round
from django.db.models import Avg
from django.core.cache import cache

# Create your views here.

from rest_framework.viewsets import ModelViewSet


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = []
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Subject.objects.all().prefetch_related('courses')

    def list(self, request, *args, **kwargs):
        cache_key = "subject_list"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = self.get_queryset()


        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        cache.set(cache_key, data, timeout=60)
        return Response(data)

    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)



class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = []
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPagination

    def get_queryset(self):
        queryset = Course.objects.select_related('subject').annotate(avg_rating=Round(Avg("comments__rating"), precision=2))
        return queryset

    def list(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', '')
        offset = request.query_params.get('offset', '')
        cache_key = f"course_list_{limit}_{offset}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            # Note: paginated_response is a Response object. Use .data to cache just the payload
            cache.set(cache_key, paginated_response.data, timeout=60)
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60)
        return Response(serializer.data)

    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []
    authentication_classes = [JWTAuthentication]


class PremiumCourses(ModelViewSet):
    queryset = Course.objects.filter(is_premium=True)
    serializer_class = CourseSerializer
    permission_classes = [CanReadPremium]
    authentication_classes = [JWTAuthentication]

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'username': user.username,
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'logged_in':True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)


class JWTLogOutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer