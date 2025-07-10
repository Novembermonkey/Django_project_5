from django.urls import path, include
from rest_framework import routers
from courses import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from courses.views import JWTLogOutView

app_name = 'courses'

router = routers.DefaultRouter()
router.register(r'subjects', views.SubjectViewSet, basename='subjects')
router.register(r'courses', views.CourseViewSet, basename='courses')
router.register(r'comments', views.CommentViewSet, basename='comments')
router.register(r'premium_courses', views.PremiumCourses, basename='premium_courses')

urlpatterns = [
           path('', include(router.urls)),
           path('register/', views.RegisterView.as_view(), name='register'),
           path('login/', views.LoginView.as_view(), name='login'),
           path('logout/', views.LogoutView.as_view(), name='logout'),
           path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
           path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
           path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
           path('api/token/logout/', JWTLogOutView.as_view(), name='jwt_logout'),
]