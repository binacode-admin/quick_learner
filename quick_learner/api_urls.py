from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include('quick_user.api_urls')),
    path('courses/', include('learner_course.api_urls')),
]
