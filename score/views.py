import datetime
import threading
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import ScoreRecord, ScoreAverage
from .forms import ScoreForm
from article.models import Article


class SaveScoreAVG(threading.Thread):
    """
    program: 多线程保存平均数
    """
    def __init__(self, content_type, object_id, scored, content_object, fail_silently=False):
        self.content_type = content_type
        self.object_id = object_id
        self.scored = scored
        self.content_object = content_object
        threading.Thread.__init__(self)

    def run(self):
        if not ScoreAverage.objects.filter(
                content_type=self.content_type, object_id=self.object_id).exists():
            score_average = ScoreAverage()
            score_average.content_object = self.content_object
            score_average.average = self.scored
            score_average.count = 1
            score_average.save()
        else:
            score_average = ScoreAverage.objects.get(
                content_type=self.content_type, object_id=self.object_id)
            get_score_record = ScoreRecord.objects.filter(
                content_type=self.content_type, object_id=self.object_id)
            scored_num = 0
            for i in range(len(get_score_record)):
                scored_num += get_score_record[i].scored_num
            score_average.count = get_score_record.count()
            score_average.average = scored_num / get_score_record.count()
            score_average.save()


def save_score(score_form, content_type):
    """
    :param score_form: 保存打分记录
    :return: status
    """
    status = 'SUCCESS'
    try:
        score_record = ScoreRecord()
        score_record.scored_num = score_form.cleaned_data['scored']
        score_record.text = score_form.cleaned_data['text']
        score_record.user = score_form.cleaned_data['user']
        score_record.content_object = score_form.cleaned_data['content_object']
        score_record.save()
        # 保存总数据
        save_score_avg = SaveScoreAVG(
            content_type,
            score_form.cleaned_data['object_id'],
            score_form.cleaned_data['scored'],
            score_form.cleaned_data['content_object']
        )
        save_score_avg.start()
    except:
        status = 'ERROR'
    return status


def add_score(request):
    # 检查通过保存数据
    data = {}
    content_type = ContentType.objects.get_for_model(Article)
    score_form = ScoreForm(request.POST, user=request.user)
    if score_form.is_valid():
        # 用户不是第一次打分
        if ScoreRecord.objects.filter(
                content_type=content_type,
                object_id=score_form.cleaned_data['object_id'],
                user=score_form.cleaned_data['user']).exists():
            last_score = ScoreRecord.objects.filter(
                content_type=content_type,
                object_id=score_form.cleaned_data['object_id'],
                user=score_form.cleaned_data['user']).order_by('-id').first()
            again_score_time = (datetime.date.today() - last_score.scored_time).days
            # 打分时限
            if again_score_time > 7:
                data['status'] = save_score(score_form, content_type)
            else:
                data['message'] = '{0}天后可再次打分'.format(
                    7 - again_score_time if 7 - again_score_time > 0 else 1)
        # 第一次打分
        else:
            data['status'] = save_score(score_form, content_type)
    else:
        data['status'] = 'ERROR'
        data['message'] = list(score_form.errors.values())[0][0]
    return JsonResponse(data)
