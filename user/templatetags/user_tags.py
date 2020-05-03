from urllib.parse import urlencode
from django import template
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from article_statistics.models import ParticipateCount

register = template.Library()


@register.simple_tag
def get_login_by_qq():
    params = {
        'response_type': 'code',
        'client_id': settings.WB_APP_KEY,
        'redirect_uri':  settings.WB_REDIRECT_URL,
    }
    return 'https://api.weibo.com/oauth2/authorize?' + urlencode(params)


# @register.simple_tag
# def get_login_by_qq():
#     params = {
#         'response_type': 'code',
#         'client_id': settings.QQ_APP_ID,
#         'redirect_uri':  settings.QQ_REDIRECT_URL,
#         'state': settings.QQ_STATE
#     }
#     return 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)
