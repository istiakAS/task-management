from django.shortcuts import render
from django.http import HttpResponse
from tasks.form import TaskForm, TaskModelForm
from .models import Task

# Create your views here.
def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    return render(request, "test.html")

from .models import Employee

def create_task(request):
    # employees = Employee.objects.all()  # get data from DB
    form = TaskModelForm()  # pass data to form

    if request.method == 'POST':
        form = TaskModelForm(request.POST)
        if form.is_valid():

            """for model form data"""
            form.save()  # save data to DB

            return render(request, 'task_from.html', {'form': form, 'message': "Task added successfully!"})

    context = {
        "form": form
    }
    return render(request, "task_from.html", context)

def view_task(request):
    tasks = Task.objects.all()  # get data from DB

    #retrive a specific task
    task3 = Task.objects.get(id=3)
    return render(request, "show_task.html", {"tasks": tasks, "task3": task3})  # pass data to template
