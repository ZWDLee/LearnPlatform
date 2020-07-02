from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord

register = template.Library()


@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model


@register.simple_tag
def get_like_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    if LikeCount.objects.filter(content_type=content_type, object_id=obj.pk).exists():
        like_count = LikeCount.objects.get(content_type=content_type, object_id=obj.pk)
        return like_count.liked_num
    else:
        return 0


@register.simple_tag(takes_context=True)
def get_likes_style(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    try:
        user = context['user']
        if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
            return True
        else:
            return False
    except:
        return False
