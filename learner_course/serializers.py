from rest_framework import serializers
from .models import LearnerCourse


class LearnerCourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerCourse
        fields = ['name', 'description', 'cover_image']
