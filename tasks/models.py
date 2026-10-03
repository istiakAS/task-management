from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



# Create your models here.



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

    # assigned_to = models.ManyToManyField(Employee, related_name='tasks')  #many to many relationship with employee model
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
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
    asset = models.ImageField(upload_to='tasks_asset', blank=True, null=True,
                              default="tasks_asset/default.jpg")
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

