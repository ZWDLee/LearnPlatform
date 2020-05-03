from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_notifications, name='my_notifications'),
    path('notification_read/', views.notification_read, name='notification_read'),
    path('system_notification/<int:notification_id>', views.system_notification, name='system_notification'),
    path('delete_notifications/', views.delete_notifications, name='delete_notifications')
]