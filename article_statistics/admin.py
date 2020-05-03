from django.contrib import admin
from .models import ParticipateRecord, ParticipateCount


@admin.register(ParticipateRecord)
class ParticipateRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'participate', 'user', 'participate_time')


@admin.register(ParticipateCount)
class ParticipateCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'participate_num')