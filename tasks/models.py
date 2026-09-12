from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail


# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
    ]
    project = models.ForeignKey(
        "Project", 
        on_delete=models.CASCADE,
        default=1
    )  #one to many relationship with project model

    assigned_to = models.ManyToManyField(Employee, related_name='tasks')  #many to many relationship with employee model
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title

# one to one ba one to many relationship a alaways child a relation bosate hoi

class TaskDetails(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    task = models.OneToOneField(Task, on_delete=models.DO_NOTHING, related_name = 'details')  #one to one relationship with Task model
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details for Task: {self.task.title}"

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name

#signals

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_assignment(sender, instance, action, **kwargs):
    if action == "post_add":
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        send_mail(
            "New Task Assigned",
            f"You have been assigned a new task: {instance.title}",
            "istiakah32@gmail.com",
            assigned_emails,
            fail_silently=False
        )

@receiver(post_save, sender=Task)
def delete_associate_details(sender, instance, **kwargs):
    if hasattr(instance, 'details'):
        print(instance)
        instance.details.delete()
        print("Deleted successfully")