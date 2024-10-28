import os
import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from quick_user.models import QuickUser


def unique_video_filename(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("videos/", unique_filename)


class LearnerCourse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="course_covers/", blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    trainer = models.ForeignKey(
        QuickUser, on_delete=models.CASCADE, related_name="courses_taught"
    )
    students = models.ManyToManyField(
        QuickUser, related_name="courses_enrolled", blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']


class CourseContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        LearnerCourse, on_delete=models.CASCADE, related_name="contents"
    )
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    watch_order = models.PositiveIntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.course.name} - {self.title} ({self.content_type})"

    class Meta:
        ordering = ['date_created']


class VideoContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_file = models.FileField(upload_to=unique_video_filename)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Video Content - {self.video_file.name}"


class ImageContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_file = models.ImageField(upload_to="images/")
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image Content - {self.image_file.name}"


class TextContent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()

    def __str__(self):
        return "Text Content"


class ObjectiveQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.ForeignKey(CourseContent, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text


class ObjectiveOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(ObjectiveQuestion, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Option for '{self.question.question_text}': {self.option_text}"