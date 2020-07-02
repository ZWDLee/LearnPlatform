from django.urls import path
from . import views
from . import utils

urlpatterns = [
    path('login/', views.login_to, name='login_to'),
    path('register/', views.register, name='register'),
    path('active/', views.active, name='active'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('send_verification_code/', utils.send_verification_code, name='send_verification_code'),
    path('logout/', views.logout_to, name='logout_to'),
    path('verification_code/', utils.verification_code, name='verification_code'),
    path('center/<int:user_center_pk>/', views.user_center, name='user_center'),
    path('profile/', views.user_profile, name='user_profile'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('change_password/', views.change_password, name='change_password'),
    path('save_user_profile/', views.save_user_profile, name='save_user_profile'),
    path('change_introduction/', views.change_introduction, name='change_introduction'),
    path('article_type_select/', views.article_type_select, name='article_type_select'),
    path('login_by_qq', views.login_by_qq, name='login_by_qq')
]