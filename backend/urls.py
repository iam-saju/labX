from django.urls import path,include
from .views import hello
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('hello', hello),
    path('',include('tl_app.urls')),
 # OAuth URLs
]


# Serve uploaded files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)