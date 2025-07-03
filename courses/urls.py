from os.path import basename

from django.urls import path, include
from rest_framework import routers

from courses import views


app_name = 'courses'

router = routers.DefaultRouter()
router.register(r'subjects', views.SubjectViewSet, basename='subjects')
router.register(r'courses', views.CourseViewSet, basename='courses')
router.register(r'comments', views.CommentViewSet, basename='comments')

urlpatterns = [
           path('', include(router.urls)),
]