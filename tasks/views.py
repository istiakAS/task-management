from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from .models import Task, TaskDetails, Project
from datetime import date
from django.db.models import Count, Avg, Sum, Min, Max, Q
from django.contrib import messages

# Create your views here.
def manager_dashboard(request):
    
    # getting task count 
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status="PENDING").count()

    # count = {
    #     "total_task": tasks.count(),
    #     "completed_task": Task.objects.filter(status="COMPLETED").count(),
    #     "in_progress_task": Task.objects.filter(status="IN_PROGRESS").count(),
    #     "pending_task": Task.objects.filter(status="PENDING").count(),
    # }
    type = request.GET.get('type', 'all')  # get the value of the 'type' parameter from the request, default to 'all' if not provided
    # print(type)

    tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all()  # get data from DB

    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status="PENDING"))

    )

    # retriving data

    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()

    context = {
        "tasks": tasks,
        "counts": counts
    
    }
    return render(request, "dashboard/manager-dashboard.html", context)

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    return render(request, "test.html")

from .models import Employee

def create_task(request):
    # employees = Employee.objects.all()  # get data from DB
    task_form = TaskModelForm()  # pass data to form
    task_detail_form = TaskDetailModelForm()  # pass data to form

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST) 
        task_detail_form = TaskDetailModelForm(request.POST) 

        if task_form.is_valid() and task_detail_form.is_valid():

            """for model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task  # set the task for the task detail
            task_detail.save()  # save the task detail

            messages.success(request, "Task created successfully!")
            return redirect('create-task')  # redirect to the same page after successful submission

    context = {
        "task_form": task_form,
        "task_detail_form": task_detail_form
    }
    return render(request, "task_from.html", context)

def update_task(request, id):
    # employees = Employee.objects.all()  # get data from DB
    task = Task.objects.get(id=id)  # get the task instance to update
    task_form = TaskModelForm(instance=task)  # pass data to form
    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)  # pass data to form

    if request.method == 'POST':
        
        task_form = TaskModelForm(request.POST, instance=task)  # bind the form to the existing task instance
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)  # bind the form to the existing task details instance

        if task_form.is_valid() and task_detail_form.is_valid():

            """for model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task  # set the task for the task detail
            task_detail_form.save()  # save the task detail

            messages.success(request, "Task updated successfully!")
            return redirect('update-task', id=task.id)  # redirect to the same page after successful submission

    context = {
        "task_form": task_form,
        "task_detail_form": task_detail_form
    }
    return render(request, "task_from.html", context)

def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('manager-dashboard')  # redirect to the manager dashboard after deletion
    else:
        messages.error(request, "Something went wrong!")
        return redirect('manager-dashboard')  # redirect to the manager dashboard if not a POST request


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
