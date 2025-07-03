
from django.contrib import admin
from .models import Course, Subject, Comment

# Register your models here.

models = [Subject, Course, Comment]

admin.site.register(models)