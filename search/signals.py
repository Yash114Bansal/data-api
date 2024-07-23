
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Startup, EmailTemplate
from django.conf import settings
import requests
from django.core.exceptions import ValidationError

def sendWhatsappMessage(phone, status, language):
    if language is None:
        language = 'english'
    else:
        language = 'hindi' if 'hin' in language else 'english'
    data = {
            "apiKey": settings.SERRI_API_KEY,
            "destination": f"+91{phone}",
            "campaignName": f"{status}_{language}"
        }
    url = "https://backend.api-wa.co/campaign/serri-india/api/v2"

    requests.post(url=url, data=data)

def sendEmail(startup_instance: Startup):
    startup_email = startup_instance.email
    try:
        email_template = EmailTemplate.objects.get(status=startup_instance.current_status)
    except EmailTemplate.DoesNotExist:
        return
    
    email_subject = email_template.subject
    email_body = email_template.body
    email_body = email_body.replace("{{name}}", startup_instance.name)
    # email_body = email_body.replace("{{link}}", email_template.link)

    send_mail(subject=email_subject, message=email_body, from_email=settings.EMAIL_HOST_USER, recipient_list=[startup_email])

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
            sendWhatsappMessage(phone_number, instance.current_status, instance.language)
