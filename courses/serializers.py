from rest_framework import serializers
from courses.models import Subject, Course, Comment
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


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






class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials")
