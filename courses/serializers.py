from tkinter.tix import Select

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from courses.models import Subject, Course, Comment
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth import authenticate






class CourseSerializer(serializers.ModelSerializer):
    subject_title = serializers.StringRelatedField(source='subject.title')
    subject_slug = serializers.SlugRelatedField(
        source = 'subject',
        slug_field = 'slug',
        read_only = True
    )
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class CourseTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title']

class SubjectSerializer(serializers.ModelSerializer):
    courses = CourseTitleSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        exclude = ('slug',)

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



class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'is_staff': self.user.is_staff,
        }

        return data
