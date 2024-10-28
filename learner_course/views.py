from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import LearnerCourse
from .serializers import LearnerCourseCreateSerializer


class IsTrainer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_category == "Trainer"


class LearnerCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = LearnerCourseCreateSerializer
    permission_classes = [IsTrainer]

    def perform_create(self, serializer):
        serializer.save(trainer=self.request.user)