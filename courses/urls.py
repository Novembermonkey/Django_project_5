from django.urls import path, include
from rest_framework import routers

from courses import views


app_name = 'courses'

router = routers.DefaultRouter()
router.register(r'subjects', views.SubjectViewSet, basename='subjects')
router.register(r'courses', views.CourseViewSet, basename='courses')
router.register(r'comments', views.CommentViewSet, basename='comments')
router.register(r'premium_courses', views.PremiumCourses, basename='premium_courses')

urlpatterns = [
           path('', include(router.urls)),
]