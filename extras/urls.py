from django.urls import path
from . import views

urlpatterns = [
    path('whatsapp/', views.whatsappWebhook, name='whatsapp-webhook'),
]