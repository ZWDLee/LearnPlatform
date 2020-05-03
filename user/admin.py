from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'nickname', 'icon', 'gender', 'birth', 'user_type', 'education', 'introduction')
