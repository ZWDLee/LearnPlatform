import datetime
from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from ..models import ScoreRecord
from ..forms import ScoreForm
from article_statistics.models import ParticipateRecord

register = template.Library()


@register.simple_tag
def get_score_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = ScoreForm(initial={
        'content_type': content_type,
        'object_id': obj.pk,
        'scored': 0
    })
    return form


@register.simple_tag(takes_context=True)
def get_score_list(context, obj):
    page_num = context['request'].GET.get('page', 1)
    content_type = ContentType.objects.get_for_model(obj)
    score_list = ScoreRecord.objects.filter(content_type=content_type, object_id=obj.pk)
    paginator = Paginator(score_list, 15)
    page_of_data = paginator.get_page(page_num)
    # 当前页面前后各两页
    current_page = page_of_data.number
    all_page = paginator.num_pages
    page_range = range(max(current_page - 2, 1) if current_page >= 2 else current_page,
                       current_page + 3 if current_page <= all_page - 2 else all_page + 1)
    # 加上省略标点
    page_list = list(page_range)
    if page_list[0] - 1 >= 2:
        page_list.insert(0, '...')
    if all_page - page_list[-1] >= 2:
        page_list.append('...')
        # 加上首页尾页
    if page_list[0] != 1:
        page_list.insert(0, 1)
    if page_list[-1] != all_page:
        page_list.append(all_page)
    context['paginator'] = paginator
    context['page_of_data'] = page_of_data
    context['page_list'] = page_list
    return context


@register.simple_tag
def get_parti_time_to_now(obj):
    content_type = ContentType.objects.get_for_model(obj)
    score_list = ScoreRecord.objects.filter(content_type=content_type, object_id=obj.pk).order_by('-id')[:10]
    parti_time_to_now = {}
    for i in range(len(score_list)):
        parti_time_to_now.update(
            {score_list[i].object_id: datetime.date.today().__sub__(ParticipateRecord.objects.get(
                content_type=content_type,
                object_id=obj.pk,
                user=score_list[i].user).participate_time).days})
    return parti_time_to_now


@register.filter
def get_range(value):
    return range(int(value))


@register.filter
def get_sub(value):
    return 5 - int(value)
