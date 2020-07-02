"""learnPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', views.home, name='home'),
    path('article/', include('article.urls')),
    path('statistics/', include('article_statistics.urls')),
    path('user/', include('user.urls')),
    path('comment/', include('comment.urls')),
    path('likes/', include('likes.urls')),
    path('score/', include('score.urls')),
    path('search/', views.search, name='search'),
    path('my_notifications/', include('my_notifications.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('notifications/', include('notifications.urls', namespace='notifications'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)