import xadmin
from .models import ParticipateRecord, ParticipateCount, IndexWheels


class ParticipateRecordAdmin(object):
    list_display = ['id', 'get_article', 'user', 'participate', 'participate_time']
    search_fields = ['id', 'user__username', 'participate_time']
    list_filter = ['user']


class ParticipateCountAdmin(object):
    list_display = ['id', 'get_article', 'participate_num']


class IndexWheelsAdmin(object):
    list_display = ['id', 'name', 'trackid']
    search_fields = ['id', 'name', 'trackid__title']


xadmin.site.register(ParticipateRecord, ParticipateRecordAdmin)
xadmin.site.register(ParticipateCount, ParticipateCountAdmin)
xadmin.site.register(IndexWheels, IndexWheelsAdmin)
