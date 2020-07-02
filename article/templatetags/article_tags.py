from django import template
from ..models import ArticleDetail

register = template.Library()


@register.simple_tag
def get_course_lesson(obj):
    if ArticleDetail.objects.filter(object_id=obj.pk).exists():
        course_lesson = ArticleDetail.objects.filter(object_id=obj.pk).last()
        return course_lesson.num
    else:
        return 0
