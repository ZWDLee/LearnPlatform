from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:article_pk>', views.article_detail, name='article_detail'),
    path('article_text/<int:article_text_pk>', views.article_text, name='article_text'),
    path('editor_course/', views.editor_course, name='editor_course'),
    path('editor_course/<int:add_course_pk>', views.editor_course, name='editor_course'),
    path('about_course/<int:course_pk>', views.about_course, name='about_course'),
    path('editor_lesson/', views.editor_lesson, name='editor_lesson'),
    path('editor_lesson/<int:lesson_pk>', views.editor_lesson, name='editor_lesson'),
]