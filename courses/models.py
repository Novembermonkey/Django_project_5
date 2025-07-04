# Create your models here.


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.db.models import Avg
from django.db.models.functions import Round
from django.contrib.auth.models import User


# Create your models here.


class Subject(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='subjects/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    duration = models.DurationField(default=timedelta(hours=12), blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    owner = models.ForeignKey(User, related_name='user_courses', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='course/images', null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    created = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def avg_rating(self):
        avg = self.comments.aggregate(avg=Round(Avg('rating'), precision=2))['avg']
        return avg


class Module(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class ItemBase(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Text(ItemBase):
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Video(ItemBase):
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def clean(self):
        super().clean()
        if self.video_file and self.url:
            raise ValidationError("Please upload only video_file or url, not both at once")

        if not self.video_file and not self.url:
            raise ValidationError("Please upload either video file or url")

    @property
    def get_video_source(self):
        if self.url:
            if "youtube.com/watch" in self.url:
                return self.url.replace("watch?v=", "embed/")
            return self.url
        elif self.video_file:
            return self.video_file.url
        return None

    def __str__(self):
        return self.title


class Image(ItemBase):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title


class File(ItemBase):
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module = models.ForeignKey(Module,
                               related_name='lessons',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file',
                                     )}
                                     )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['my_order']


class Comment(models.Model):
    class RatingChoices(models.IntegerChoices):
        ZERO = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    topic = models.TextField(blank=True, null=True)
    content = models.TextField()
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.THREE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.topic


