from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from quick_learner import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quick_learner.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
