from django.shortcuts import render
from django.http import JsonResponse
from django.db.models.fields import exceptions
from django.contrib.contenttypes.models import ContentType
from .models import ParticipateRecord, ParticipateCount
from article.models import Article


def participate_article(request):
    data = {}
    article_pk = request.GET.get('article_pk')
    user = request.user
    article = Article.objects.get(pk=article_pk)
    content_type = ContentType.objects.get_for_model(article)
    if Article.objects.filter(pk=article_pk).exists():
        try:
            parti_record, created = ParticipateRecord.objects.get_or_create(
                content_type=content_type, object_id=article_pk, user=user)
            # 参加记录如果为新建的说明用户第一次参加该课程
            parti_count, count_created = ParticipateCount.objects.get_or_create(content_type=content_type,
                                                                                object_id=article_pk)
            if created:
                # 某一课程的总参加人数加一
                parti_count.participate_num += 1
                parti_count.save()
                data['all_participate_num'] = parti_count.participate_num
                data['message'] = '参加成功'
                data['code'] = 200
            # 用户已经参加过该课程，可能在做退出课程后再次加入课程的操作
            else:
                # 参加退出的课程
                if parti_record.participate == 0:
                    # 再次加入退出的课程
                    parti_record.participate = 1
                    parti_record.save()
                    # 总参加数+1
                    parti_count.participate_num += 1
                    parti_count.save()
                    data['all_participate_num'] = parti_count.participate_num
                    data['message'] = '参加成功'
                    data['code'] = 200
                else:
                    # 参加参加的课程
                    data['message'] = '不要重复参加'
                    data['code'] = 201
            data['status'] = 'SUCCESS'
            data['article_pk'] = article_pk
        except exceptions.ObjectDoesNotExist:
            data['status'] = 'ERROR'
            data['message'] = exceptions.ObjectDoesNotExist
    else:
        data['status'] = 'ERROR'
        data['message'] = exceptions.ObjectDoesNotExist
    return JsonResponse(data)


def drop_out_article(request):
    data = {}
    article_pk = request.GET.get('article_pk')
    user = request.user
    content_type = ContentType.objects.get_for_model(Article)
    if Article.objects.filter(pk=article_pk).exists():
        try:
            participate_record = ParticipateRecord.objects.get(
                content_type=content_type, object_id=article_pk, user=user)
            participate_count = ParticipateCount.objects.get(
                content_type=content_type, object_id=article_pk)
            if participate_record.participate == 1:
                participate_record.participate = 0
                participate_record.save()
                participate_count.participate_num -= 1
                participate_count.save()
                data['all_participate_num'] = participate_count.participate_num
                data['message'] = '退出成功'
                data['code'] = 200
            else:
                data['message'] = '重复操作'
                data['code'] = 201
            data['status'] = 'SUCCESS'
            data['article_pk'] = article_pk
        except exceptions.ObjectDoesNotExist:
            data['data'] = 'ERROR'
            data['message'] = exceptions.ObjectDoesNotExist
    return JsonResponse(data)
