import xadmin
from .models import LikeRecord, LikeCount


class LikeRecordAdmin(object):
    list_display = ['id', 'get_comment', 'user', 'liked_time']
    search_fields = ['id', 'user__name', 'liked_time']
    list_filter = ['user']


class LikeCountAdmin(object):
    list_display = ['id', 'get_comment', 'liked_num']
    list_filter = ['liked_num']


xadmin.site.register(LikeRecord, LikeRecordAdmin)
xadmin.site.register(LikeCount, LikeCountAdmin)
