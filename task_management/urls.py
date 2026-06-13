
from django.contrib import admin
from django.urls import path,manager_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manager-dashboard/', manager_dashboard),
]
