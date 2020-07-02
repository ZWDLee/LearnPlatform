from django.shortcuts import render
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm
from article.models import Article


def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        parent = comment_form.cleaned_data['parent']
        # 判断是评论还是回复
        if parent is not None:
            # 是回复时
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        # 返回数据
        data['status'] = 'SUCCESS'
        data['user_pk'] = comment.user.pk
        data['user_avatar'] = comment.user.get_user_icon()
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if parent is not None:
            data['reply_to_key'] = comment.reply_to.pk
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)


def get_user_center(comments):
    data = {}
    data['user_pk'] = {}
    data['user_name'] = {}
    data['user_avatar'] = {}
    for i in range(len(comments)):
        data['user_pk'].update({i: comments[i].user.pk})
        data['user_name'].update(
            {i: comments[i].user.profile.nickname if comments[i].user.profile.nickname else comments[i].user.username})
        data['user_avatar'].update({i: comments[i].user.profile.icon.url})
    return data


def page_control(request):
    pass