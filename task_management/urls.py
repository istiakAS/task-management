
from django.contrib import admin
from django.urls import path,include
from tasks.views import home
from tasks.views import contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", home),
    path("contact/", contact),
    path("tasks/", include("tasks.urls"))
]
