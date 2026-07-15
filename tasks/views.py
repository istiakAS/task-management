from django.shortcuts import render
from django.http import HttpResponse
from tasks.form import TaskForm, TaskModelForm
from .models import Task, TaskDetails, Project
from datetime import date
from django.db.models import Count, Avg, Sum, Min, Max

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
    # Show the status that are completed 
    # tasks = Task.objects.filter(status="COMPLETED")  # get data from DB

    # show today date 
    # tasks = Task.objects.filter(due_date=date.today())   # get data from DB

    # tasks = TaskDetails.objects.exclude(priority="L")
    # tasks = TaskDetails.objects.select_related('task').all()
    # tasks = Task.objects.select_related('project').all() # get data from DB

    # tasks = Project.objects.prefetch_related('task_set').all()  # get data from DB


    # tasks = Task.objects.prefetch_related('assigned_to').all()  # get data from DB

    """Aggregation """

    projects = Project.objects.annotate(num_tasks=Count('task')).order_by('num_tasks')  # get data from DB

    return render(request, "show_task.html", {"projects": projects})  # pass data to template
