from django.template.defaulttags import comment
from rest_framework import serializers
from courses.models import Subject, Course, Comment
from django.db.models import Avg
from django.db.models.functions import Round


class SubjectSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        exclude = ('slug',)

    def get_courses(self, obj):
        return list(obj.courses.values_list('title', flat=True))


class CourseSerializer(serializers.ModelSerializer):
    subject_title = serializers.StringRelatedField(source='subject.title')
    subject_slug = serializers.SlugRelatedField(
        source = 'subject',
        slug_field = 'slug',
        read_only = True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_rating(self, obj):
        avg = obj.comments.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 2) if avg is not None else 0


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
