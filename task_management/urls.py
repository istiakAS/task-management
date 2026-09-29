from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home, no_permissions
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),
    path("users/", include("users.urls")),
    path('', home, name='home'),
    path('no_permissions/', no_permissions, name='no_permissions'),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )