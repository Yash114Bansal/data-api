
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Startup
from .utils import sendWhatsappMessage, sendEmail

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
            sendEmail(instance)
        phone_number = instance.mobile_number
        if phone_number is None:
            phone_number = instance.additional_number
        if phone_number:
            sendWhatsappMessage(phone_number, instance)
