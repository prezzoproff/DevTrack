from django.urls import path
from . import views

urlpatterns = [
    path('issues_page/', views.issues_page, name='issuespage'),
    path('ai_assistant/', views.ai_assistant_view, name = 'ai_assistant'),
]