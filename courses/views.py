from .models import Subject, Course, Comment
from .permissions import *
from .serializers import SubjectSerializer, CourseSerializer, CommentSerializer
from rest_framework.generics import ListAPIView
# Create your views here.

from rest_framework.viewsets import ModelViewSet


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [EvenYearsOnly]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [SuperUserOnly]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [UpdateOnly]


class PremiumCourses(ModelViewSet):
    queryset = Course.objects.filter(is_premium=True)
    serializer_class = CourseSerializer
    permission_classes = [CanReadPremium]
