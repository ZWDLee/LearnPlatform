from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import ParticipateCount

register = template.Library()


@register.simple_tag
def get_participate_num(obj):
    content_type = ContentType.objects.get_for_model(obj)
    if ParticipateCount.objects.filter(content_type=content_type, object_id=obj.pk).exists():
        participate = ParticipateCount.objects.get(content_type=content_type, object_id=obj.pk)
        return participate.participate_num
    else:
        return 0
