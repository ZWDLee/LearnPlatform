from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from article_statistics.models import ParticipateRecord


class ScoreForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    scored = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control',
               'rows': '3',
               'placeholder': '客观评价，文明用语!'}),
        label='',
        max_length=100,
        min_length=10
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ScoreForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        # 评论对象是否合理验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        if content_type == '课程':
            content_type = 'article'
        try:
            score_class = ContentType.objects.get(model=content_type).model_class()
            score_obj = score_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = score_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')
        # 是否参与了该课程
        try:
            participate_content_type = ContentType.objects.get(model=content_type)
            ParticipateRecord.objects.get(
                content_type=participate_content_type,
                object_id=object_id,
                user=self.user,
                participate=True
            )
        except ObjectDoesNotExist:
            raise forms.ValidationError('请先参加课程')
        return self.cleaned_data

    def clean_scored(self):
        scored = self.cleaned_data['scored']
        if scored < 0:
            raise forms.ValidationError('分数错误')
        if scored == 0:
            raise forms.ValidationError('未打分，请打分')
        return scored
