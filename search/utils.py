from django.core.mail import send_mail
from django.conf import settings

from extras.models import MessageStatusInfo
from .models import Startup, EmailTemplate
from django.conf import settings
import requests
from django.core.exceptions import ValidationError

def generateID(startup_instance: Startup):
    pk = startup_instance.pk

    id = f"NB{str(pk).zfill(10)}"

    return id


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

    founder_name = startup_instance.founder_name
    startup_name = startup_instance.name
    application_id = generateID(startup_instance)
    template_params = [
                f"*{founder_name}*",
                f"*{application_id}*",
                f"*{startup_name}*",
            ]
    if "rejected" in status or "knockout" in status:
        template_params = [f"*{founder_name}*",]

    data = {
            "apiKey": settings.SERRI_API_KEY,
            "destination": f"+91{phone}",
            "campaignName": f"new_{status}_{language}",
            "templateParams": template_params,
        }
    url = "https://backend.api-wa.co/campaign/serri-india/api/v2"
    
    r = requests.post(url=url, json=data)
    request = r.request

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