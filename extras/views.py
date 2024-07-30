import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from .models import MessageStatusInfo

@csrf_exempt
def whatsappWebhook(request):
    if request.method == 'POST':
        print(f'{datetime.now()} - Received a POST Webhook request, Data: {request.body}')

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            print(f'{datetime.now()} - Invalid JSON data received')
            return HttpResponse(status=400)
        try:
            message_id = data["data"]["message"]["submitted_message_id"]
            new_status = data["data"]["message"]["status"]
        except KeyError:
            print(f'{datetime.now()} - Invalid JSON data received')
            return HttpResponse(status=400)
        
        update_status(message_id, new_status)
        
        return HttpResponse(status=200)
    
    else:
        return HttpResponse(status=405)

def update_status(message_id, new_status):
    try:
        message_status_info = MessageStatusInfo.objects.get(message_id=message_id)
        orignal_status = message_status_info.sent_status
        status_priority = {
            'sent': 3,
            'delivered': 2,
            'pending': 1,
            'failed': 0
        }
        try:
            if status_priority[new_status] < status_priority[orignal_status]:
                return
    
        except KeyError:
            print(f'{datetime.now()} - Invalid status received: {new_status}')

        print(f'{datetime.now()} - Updating status of message_id {message_id} to {new_status}')
    except MessageStatusInfo.DoesNotExist:
        print(f'{datetime.now()} - MessageStatusInfo with message_id {message_id} not found')
        return
    
    message_status_info.sent_status = new_status
    message_status_info.save()