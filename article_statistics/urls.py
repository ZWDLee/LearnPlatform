from django.urls import path
from . import views

urlpatterns = [
    path('participate_article/', views.participate_article, name='participate_article'),
    path('drop_out_article/', views.drop_out_article, name='drop_out_article'),
]