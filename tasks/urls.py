from django.urls import path
from tasks.views import (
    manager_dashboard,
    user_dashboard,
    test,
    create_task,
    view_task,
    update_task,
    delete_task,
)

urlpatterns = [
    path("manager-dashboard/", manager_dashboard, name="manager-dashboard"),
    path("user-dashboard/", user_dashboard, name="user-dashboard"),
    path("test/", test, name="test"),
    path("create-task/", create_task, name="create-task"),
    path("view-task/", view_task, name="view-task"),
    path("update-task/<int:id>/", update_task, name="update-task"),
    path("delete-task/<int:id>/", delete_task, name="delete-task"),
]