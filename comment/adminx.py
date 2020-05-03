import xadmin
from .models import Comment


class CommentAdmin(object):
    list_display = ['id', 'get_article', 'user', 'root', 'parent', 'reply_to', 'comment_time']
    search_fields = ['id', 'user__username', 'root__text', 'parent__text', 'reply_to__username', 'comment_time']
    list_filter = ['user', 'reply_to', 'comment_time']


xadmin.site.register(Comment, CommentAdmin)
