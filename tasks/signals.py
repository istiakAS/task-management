from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task


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