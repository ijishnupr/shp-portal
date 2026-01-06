# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-site/', views.add_survey, name='add_survey'),
    path('register/', views.register, name='register'), # <-- Added this
]