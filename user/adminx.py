import xadmin
from .models import Profile


class ProfileAdmin(object):
    list_display = ['id', 'user', 'nickname', 'icon', 'gender', 'birth', 'user_type', 'education']
    search_fields = ['id', 'user_username', 'nickname']
    list_filter = ['gender', 'birth', 'user_type']
    list_editable = ['nickname', 'icon', 'gender', 'birth', 'user_type', 'education']


xadmin.site.register(Profile, ProfileAdmin)
