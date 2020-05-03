from django.urls import path
from . import views

urlpatterns = [
    path('add_score/', views.add_score, name='add_score'),
]