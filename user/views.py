import json
import uuid
from urllib.request import urlopen
from urllib.parse import urlencode
import requests
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models.fields import exceptions
from .models import Profile
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, UserProfileForm, ChangePasswordForm, BindEmailForm
from .utils import user_status, article_all_type
from article.models import Article
from article_statistics.models import ParticipateRecord


def login_by_qq(request):
    # code = request.GET['code']
    # state = request.GET['state']
    # if state != settings.QQ_STATE:
    #     raise Exception('状态码错误')
    #
    # # 获取Access_Token
    # params = {
    #     'grant_type': 'authorization_code',
    #     'client_id': settings.QQ_APP_ID,
    #     'client_secret': settings.QQ_APP_KEY,
    #     'code': code,
    #     'redirect_uri': settings.QQ_REDIRECT_URL
    # }
    # response = urlopen('https://graph.qq.com/oauth2.0/token?' + urlencode(params))
    # data = response.read().decode('utf8')
    # access_token = parse_qs(data)['access_toke'][0]
    #
    # # 获取openid
    # response = urlopen('https://graph.qq.com/oauth2.0/me?access_token=' + access_token)
    # data = response.read().decode('utf8')
    # openid = json.loads(data[10: -4])['openid']
    # 获取access_token
    code = request.GET['code']
    params = {
        'client_id': settings.WB_APP_KEY,
        'client_secret': settings.WB_APP_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.WB_REDIRECT_URL,
        'code': code
    }
    # result = urlopen('https://api.weibo.com/oauth2/access_token?' + urlencode(params))
    result = requests.post('https://api.weibo.com/oauth2/access_token', data=params)
    data = json.loads(result.text)
    print(data)
    uid = data['uid']
    access_token = data['access_token']
    params = {
        'access_token': access_token,
        'uid': uid,
    }
    user_info = urlopen('https://api.weibo.com/2/users/show.json?' + urlencode(params))
    print(user_info)
    import pdb
    pdb.set_trace()
    # print(result)
    return HttpResponse('22')


def login_to(request):
    context = {}
    if request.method == 'POST':
        login_form = LoginForm(request.POST, request=request)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            del request.session['verification_code']
            return redirect(request.GET.get('from', reverse('home')))
        else:
            context['error_message'] = list(login_form.errors.values())[0][0]
    else:
        login_form = LoginForm(initial={'password': '123'})
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


def register(request):
    context = {}
    context['from_url'] = request.GET.get('from', '')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False)
            Profile.objects.create(user=user, nickname=username)
            if user:
                token = uuid.uuid4().hex
                cache.set('verify_email'+email, token, timeout=60*60*24)
                # 发送邮箱
                send_mail(
                    '用户注册',
                    "点击此链接进行用户激活：http://localhost:8000{0}?token={1}&email={2}，有效期1天".format(
                        reverse('active'), token, email),
                    '943318968@qq.com',
                    [email],
                )
                return redirect(reverse('login_to') +
                                '?from='+context['from_url'] if context['from_url'] is not '' else '')
    else:
        register_form = RegisterForm()
    context['register_form'] = register_form
    return render(request, 'user/register.html', context)


def active(request):
    context = {}
    email = request.GET.get('email', '')
    if request.GET.get('token', '') == cache.get('verify_email'+email):
        if User.objects.filter(email=email).exists:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            context['message'] = '激活成功'
            cache.delete('verify_email'+email)
        else:
            context['message'] = '账号不存在'
    else:
        context['message'] = '链接已过期'
    return render(request, 'user/active.html', context)


def forgot_password(request):
    if request.method == 'POST':
        forgot_password_form = ForgotPasswordForm(request.POST, request=request)
        if forgot_password_form.is_valid():
            email = forgot_password_form.cleaned_data['email']
            new_password = forgot_password_form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            del request.session['forgot_password_code']
            return redirect(reverse('login_to'))
    else:
        forgot_password_form = ForgotPasswordForm()
    context = {}
    context['forget_password_form'] = forgot_password_form
    return render(request, 'user/forget_password.html', context)


def logout_to(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))


def user_center(request, user_center_pk):
    # 用户信息
    mine = get_object_or_404(User, pk=user_center_pk)
    request_mine = request.user
    status = user_status(mine, request_mine)
    context = {}
    if status == 0 or status == 2:
        articles = Article.objects.filter(author=mine).order_by('-created_time')  # 全部的创建作品
        # 用户稿件的所有类型list
        article_list = article_all_type(articles)
        # 根据article类型筛选
        context['all_article_type'] = {}
        all_type_count = 0
        for i in range(0, len(article_list)):
            try:
                context['all_article_type'].update(
                    {str(article_list[i]): str(Article.objects.filter(author=mine).filter(
                        article_type__type_name=article_list[i]).count())})
                all_type_count += Article.objects.filter(author=mine).filter(
                    article_type__type_name=article_list[i]).count()
            except exceptions.ObjectDoesNotExist:
                context['all_article_type'] = None
        context['articles'] = articles
        context['all_type_count'] = all_type_count
    # 普通用户
    articles_list = []
    articles = ParticipateRecord.objects.filter(user=mine, participate=True)
    # # 评论
    # if Comment.objects.filter(user=request_mine).exists():
    #     comment_list = Comment.objects.filter(user=request_mine)
    # else:
    #     comment_list = None
    for i in range(len(articles)):
        articles_list.append(Article.objects.get(pk=articles[i].object_id))
    context['articles_list'] = articles_list
    context['mine'] = mine
    context['status'] = status
    # context['comment_list'] = comment_list
    return render(request, 'user/user_center.html', context)


@login_required
def user_profile(request):
    context = {}
    if not request.user.is_authenticated:
        redirect(reverse('home'))
    user = User.objects.get(pk=request.user.pk)
    context['username'] = user.username
    context['email'] = user.email
    profile = Profile.objects.get(user=user)
    user_profile_form = UserProfileForm(
        initial={'nickname': profile.nickname,
                 'gender': profile.gender,
                 'birth': profile.birth.strftime('%Y-%m-%d') if profile.birth is not None else None,
                 'education': profile.education,
                 'profile_introduction': profile.introduction})
    context['user_profile_form'] = user_profile_form
    return render(request, 'user/user_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST, user=request.user)
        if change_password_form.is_valid():
            user = request.user
            new_password = change_password_form.cleaned_data['new_password_again']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(reverse('login_to'))
    else:
        change_password_form = ChangePasswordForm()
    context = {}
    context['change_password_form'] = change_password_form
    return render(request, 'user/change_password.html', context)


def save_user_profile(request):
    data = {}
    user = request.user
    user_profile_form = UserProfileForm(request.POST, request.FILES, user=request.user)
    if user_profile_form.is_valid():
        profile = Profile.objects.get(user=user)
        profile.nickname = user_profile_form.cleaned_data['nickname']
        if user_profile_form.cleaned_data['avatar'] is not None:
            profile.icon = user_profile_form.cleaned_data['avatar']
        profile.gender = user_profile_form.cleaned_data['gender']
        profile.birth = user_profile_form.cleaned_data['birth']
        profile.education = user_profile_form.cleaned_data['education']
        profile.introduction = user_profile_form.cleaned_data['profile_introduction']
        profile.save()
        data['status'] = 'SUCCESS'
        data['message'] = '保存成功'
    else:
        data['error_message'] = list(user_profile_form.errors.values())[0][0]
        data['message'] = '保存失败'
        data['status'] = 'ERROR'
    return JsonResponse(data)


def bind_email(request):
    context = {}
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['bind_email_code']
            return redirect(reverse('user_profile'))
        else:
            context['error_message'] = list(form.errors.values())[0][0]
    else:
        form = BindEmailForm()
    context['form'] = form
    return render(request, 'user/bind_email.html', context)


@login_required
def change_introduction(request):
    data = {}
    mine_pk = request.GET.get('mine_pk')
    introduction = request.GET.get('introduction')[0:50]
    user = get_object_or_404(User, pk=mine_pk)
    if Profile.objects.filter(user=user).exists():
        old_intro = Profile.objects.get(user=user)
        if old_intro.introduction != introduction and old_intro != '':
            old_intro.introduction = introduction
            old_intro.save()
            data['status'] = 'SUCCESS'
            data['code'] = 200
            data['back_intro'] = introduction
        else:
            data['code'] = 400
    else:
        data['status'] = 'ERROR'
        data['back_intro'] = ''
    return JsonResponse(data)


def article_type_select(request):
    data = {}
    data['status'] = 'SUCCESS'
    mine_pk = request.GET.get('mine_pk')
    type_name = request.GET.get('type_name')
    mine = get_object_or_404(User, pk=mine_pk)
    if Article.objects.filter(author=mine).filter(article_type__type_name=type_name).exists():
        articles = serializers.serialize("json",
                                         Article.objects.filter(author=mine).filter(article_type__type_name=type_name))
        # 参加人数查询
        participate_len = Article.objects.filter(author=mine).filter(article_type__type_name=type_name)
        data['participate_dict'] = {}
        for i in range(len(participate_len)):
            try:
                data['participate_dict'].update({i: str(participate_len[i].participate_num.all()[0])})
            except:
                data['participate_dict'].update({i: '0'})
        if articles:
            data['code'] = 200
            data['articles'] = articles
        else:
            data['status'] = 'ERROR'
            data['message'] = '数据获取错误，请重试'
    else:
        data['code'] = 401
        data['message'] = '未创作该类型作品'
    data['article_type_name'] = type_name
    return JsonResponse(data)

