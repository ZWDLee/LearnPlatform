from django.urls import path
from . import views

urlpatterns = [
    path('update_comment/', views.update_comment, name='update_comment'),
    # path('page_control/', comment_tags.page_control, name='page_control'),
]