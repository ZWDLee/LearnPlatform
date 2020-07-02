from django.contrib import admin
from .models import ScoreRecord, ScoreAverage


@admin.register(ScoreRecord)
class ScoreRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'user', 'scored_num', 'text', 'scored_time')


@admin.register(ScoreAverage)
class ScoreAverageAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'count', 'average')
