"""
URL configuration for demo_project project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # User management
    path('accounts/', include('allauth.urls')),
    
    # Local apps
    path('', include('blog.urls')),
    path('users/', include('users.urls')),
    
    # Debug toolbar
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)