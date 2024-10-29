from rest_framework import generics, permissions

from .permissions import IsTrainer
from .serializers import LearnerCourseCreateSerializer

class LearnerCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = LearnerCourseCreateSerializer
    permission_classes = [IsTrainer]

    def perform_create(self, serializer):
        serializer.save(trainer=self.request.user)