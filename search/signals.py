
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from extras.models import MessageStatusInfo
from .models import Startup, EmailTemplate
from django.conf import settings
import requests
from django.core.exceptions import ValidationError

def sendWhatsappMessage(phone, startup_instance: Startup):
    language = startup_instance.language
    status = startup_instance.current_status

    message_status_info = MessageStatusInfo(
                startup=startup_instance,
                message_type='whatsapp',
                sent_status='pending',
                application_status = startup_instance.current_status
    )
    message_status_info.save()
    
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

    r = requests.post(url=url, data=data)

    if(r.status_code == 200):
        message_status_info.sent_status = 'sent'
        message_status_info.message_id = r.json().get('submitted_message_id')
    else:
        message_status_info.sent_status = 'failed'
        message_status_info.failed_reason = r.json().get('errorMessage')

    message_status_info.save()

def sendEmail(startup_instance: Startup):

    message_status_info = MessageStatusInfo(
                startup=startup_instance,
                message_type='email',
                sent_status='pending',
                application_status = startup_instance.current_status
    )
    message_status_info.save()

    startup_email = startup_instance.email
    try:
        email_template = EmailTemplate.objects.get(status=startup_instance.current_status)
    except EmailTemplate.DoesNotExist:
        message_status_info.sent_status = 'failed'
        message_status_info.failed_reason = 'Email template not found'
        message_status_info.save()
        return
    
    email_subject = email_template.subject
    email_body = email_template.body
    email_body = email_body.replace("{{name}}", startup_instance.name)
    if startup_instance.current_status == 'rejected':
        reason = startup_instance.rejection_message
        if reason is None:
            reason = ''
        email_body = email_body.replace("{{reason}}", reason)

    try:
        send_mail(subject=email_subject, message=email_body, from_email=settings.EMAIL_HOST_USER, recipient_list=[startup_email], fail_silently=False)
        message_status_info.sent_status = 'sent'
    except Exception as e:
        message_status_info.sent_status = 'failed'
        message_status_info.failed_reason = str(e)
    
    message_status_info.save()


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
