from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.search_company, name='search_company'),
    path('fetch-gst-turnover/', views.fetch_gst_turnover, name='fetch_gst_turnover'),
]