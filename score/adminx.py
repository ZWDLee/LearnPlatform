import xadmin
from .models import ScoreRecord, ScoreAverage


class ScoreRecordAdmin(object):
    list_display = ['id', 'user', 'scored_num', 'get_article', 'scored_time']
    search_fields = ['id', 'user__username', 'scored_num']
    list_filter = ['user', 'scored_num']


class ScoreAverageAdmin(object):
    list_display = ['id', 'get_article', 'average', 'count']


xadmin.site.register(ScoreRecord, ScoreRecordAdmin)
xadmin.site.register(ScoreAverage, ScoreAverageAdmin)
