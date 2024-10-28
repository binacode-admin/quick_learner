from django.urls import path
from .views import LearnerCourseCreateAPIView

urlpatterns = [
    path('create_course/', LearnerCourseCreateAPIView.as_view(), name='create-course'),
]
