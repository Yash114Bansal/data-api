
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Startup

@receiver(pre_save, sender=Startup)
def send_status_change_notification(sender, instance, **kwargs):
    try:
        original_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    print(original_instance.current_status , instance.current_status)
    if original_instance.current_status != instance.current_status: 
        print("SIGNAL")
        startup_email = instance.email
        if startup_email:
            subject = 'Status Change Notification'
            message = f"Dear {instance.name} Team,\n\nYour status has been changed to {instance.get_current_status_display()}.\n\nBest regards,\nABC"
            cc = [startup_email]
            if instance.email:
                cc.append(instance.email)
            send_mail(subject, message, None, [startup_email], cc)

