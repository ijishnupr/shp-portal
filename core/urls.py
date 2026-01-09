# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-site/', views.add_survey, name='add_survey'),
    path('register/', views.register, name='register'), 
    path('survey/<int:pk>/', views.view_survey_detail, name='view_survey_detail'),
     path('survey/<int:pk>/edit/', views.edit_survey, name='edit_survey'),
]