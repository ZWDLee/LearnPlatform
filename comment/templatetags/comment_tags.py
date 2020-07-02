from django import template
from django.http import JsonResponse
from django.db.models import Max
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from ..models import Comment
from ..forms import CommentForm
from likes.models import LikeCount

register = template.Library()


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={
        'content_type': content_type,
        'object_id': obj.pk,
        'reply_comment_id': 0
    })
    return form


@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment_count = Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()
    return comment_count


# def page_control(request):
#     context = {}
#     page_num = int(request.GET.get('page_num', 1))
#     article_text_pk = int(request.GET.get('article_text_pk', 1))
#     # import pdb
#     # pdb.set_trace()
#
#     comment_list = Comment.objects.filter(object_id=article_text_pk, parent=None)
#     # get_comment = comment_list[15 * (page_num - 1), min(15 * page_num, len(comment_list))]
#     context['comment_list'] = serializers.serialize("json", comment_list)
#     return JsonResponse(context)


@register.simple_tag(takes_context=True)
def get_comment_list(context, obj):
    page_num = context['request'].GET.get('page', 1)
    order = context['request'].GET.get('order', '')
    content_type = ContentType.objects.get_for_model(obj)
    comment_list = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    order_list = []
    sort_dist = {}
    if order != 'date':
        # 按点赞数排序
        # 取出数据
        for i in range(len(comment_list)):
            sort_dist.update(
                {comment_list[i]: LikeCount.objects.get(
                    object_id=comment_list[i].pk).liked_num if LikeCount.objects.filter(
                    object_id=comment_list[i].pk).exists() is True else 0}
            )
        # 排序
        sorted_dist = sorted(sort_dist.items(), key=lambda sort_dist: sort_dist[1], reverse=True)
        # 转为list
        for i in range(len(sorted_dist)):
            order_list.append(sorted_dist[i][0])
    else:
        order_list = Comment.objects.filter(
            content_type=content_type, object_id=obj.pk, parent=None).order_by('-comment_time')
    # 分页
    paginator = Paginator(order_list, 15)
    page_of_comment = paginator.get_page(page_num)
    # 当前页面前后各两页
    current_page = page_of_comment.number
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
    print(page_list)

    context = {}
    context['paginator'] = paginator
    context['page_of_comment'] = page_of_comment
    context['page_list'] = page_list
    return context


