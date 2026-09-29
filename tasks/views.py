from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from .models import Task, Project
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView





# Create your views here.

def is_manager(user):
    return user.is_superuser or user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

@user_passes_test(is_manager, login_url='no_permissions')
def manager_dashboard(request):

    type = request.GET.get('type', 'all')  # get the value of the 'type' parameter from the request, default to 'all' if not provided

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

@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


@login_required
@permission_required("tasks.add_task", login_url="no_permissions")
def create_task(request):
    # employees = Employee.objects.all()  # get data from DB
    task_form = TaskModelForm()  # pass data to form
    task_detail_form = TaskDetailModelForm()  # pass data to form

    if request.method == 'POST':
        task_form = TaskModelForm(request.POST) 
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES) 

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

# variable list of decorators
create_decorators = [login_required, permission_required("tasks.add_task", login_url="no_permissions")]

class CreateTask(ContextMixin, LoginRequiredMixin,PermissionRequiredMixin, View):
    """ for creating task"""
    permission_required = 'tasks.add_task'
    login_url = 'sign_in'
    template_name = "task_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get('task_detail_form', TaskDetailModelForm())
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data() 
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST) 
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES) 
    
        if task_form.is_valid() and task_detail_form.is_valid():
            """for model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task  # set the task for the task detail
            task_detail.save()  # save the task detail

            messages.success(request, "Task created successfully!")
            context = self.get_context_data(task_form=task_form, task_details_form=task_detail_form)
            return render(request, self.template_name, context)


# variable list of decorators
update_decorators = [login_required, permission_required("tasks.add_task", login_url="no_permissions")]

@method_decorator(update_decorators, name="dispatch")
def update_task(request, id):
    # employees = Employee.objects.all()  # get data from DB
    task = Task.objects.get(id=id)  # get the task instance to update
    task_form = TaskModelForm(instance=task)  # pass data to form
    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)  # pass data to form

    if request.method == 'POST':
        
        task_form = TaskModelForm(request.POST, instance=task)  # bind the form to the existing task instance
        task_detail_form = TaskDetailModelForm(request.POST, request.Files, instance=task.details)  # bind the form to the existing task details instance

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

# variable list of decorators
update_decorators = [login_required, permission_required("tasks.add_task", login_url="no_permissions")]

# @method_decorator(update_decorators, name="dispatch")
# class UpdateTask(View):
#     def get(self, request,id, *args, **kwargs):
#         task = Task.objects.get(id=id)  # get the task instance to update
#         task_form = TaskModelForm(instance=task)  # pass data to form
#         if task.details:
#             task_detail_form = TaskDetailModelForm(instance=task.details)  # pass data to form
#         context = {
#                 "task_form": task_form,
#                 "task_detail_form": task_detail_form
#             }
#         return render(request, "task_from.html", context)
#     def post(self, request, *args, **kwargs):
                
#         task_form = TaskModelForm(request.POST, instance=task)  # bind the form to the existing task instance
#         task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)  # bind the form to the existing task details instance

#         if task_form.is_valid() and task_detail_form.is_valid():

#             """for model form data"""
#             task = task_form.save()
#             task_detail = task_detail_form.save(commit=False)
#             task_detail.task = task  # set the task for the task detail
#             task_detail_form.save()  # save the task detail

#             messages.success(request, "Task updated successfully!")
#             return redirect('update-task', id=task.id)  # redirect to the same page after successful submission

class UpdateTask(UpdateView):
    model = Task 
    form_class = TaskModelForm 
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()

        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()
        return context 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)

        task_detail_form = TaskDetailModelForm(request.POST, request.FILES, instance=getattr(self.object, 'details', None))

        if task_form.is_valid() and task_detail_form.is_valid():
            """for model form data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task  # set the task for the task detail
            task_detail_form.save()  # save the task detail

            messages.success(request, "Task updated successfully!")
            return redirect('update-task', self.object.id)  # redirect to the same page after successful submission
        return redirect('update-task', self.object.id)



@login_required
@permission_required("tasks.delete_task", login_url="no_permissions")
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('manager-dashboard')  # redirect to the manager dashboard after deletion
    else:
        messages.error(request, "Something went wrong!")
        return redirect('manager-dashboard')  # redirect to the manager dashboard if not a POST request

@login_required
@permission_required("tasks.view_task", login_url="no_permissions")
def view_task(request):
    """Aggregation """

    projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')  # get data from DB

    return render(request, "show_task.html", {"projects": projects})  # pass data to template
view_project_decorators = [login_required, permission_required("projects.view_project", login_url="no_permissions")]

@method_decorator(view_project_decorators, name="dispatch")
class ViewProject(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'show_task.html'

    def get_queryset(self):
        queryset = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
        return queryset


@login_required
@permission_required("tasks.view_task", login_url="no_permissions")
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES


    if request.method == 'POST':
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)

        
    return render(request, 'task_details.html', {"task" : task, 'status_choices' : status_choices})

class TaskDetail(DetailView):
    model = Task 
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)


@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')

    elif is_manager(request.user):
        return redirect('manager-dashboard')

    elif is_employee(request.user):
        return redirect('user-dashboard')

    return redirect('no-permission')

