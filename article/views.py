from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from .models import Article, ArticleDetail
from .forms import EditorCourseForm, EditorLessonForm
from article_statistics.models import ParticipateRecord
from score.models import ScoreAverage, ScoreRecord
from comment.models import Comment
from likes.models import LikeCount
from my_notifications.utils import score_from_notification_into


def comment_like_from_notification_into(deal_with_pk, deal_with_list):
    order_list = []
    sort_dist = {}
    for i in range(len(deal_with_list)):
        sort_dist.update(
            {deal_with_list[i]: LikeCount.objects.get(
                object_id=deal_with_list[i].pk).liked_num if LikeCount.objects.filter(
                object_id=deal_with_list[i].pk).exists() is True else 0}
        )
        # 排序
    sorted_dist = sorted(sort_dist.items(), key=lambda sort_dist: sort_dist[1], reverse=True)
    # 转为list
    for i in range(len(sorted_dist)):
        order_list.append(sorted_dist[i][0])
    comment_page_cut = int(len(deal_with_list) / 15) if len(deal_with_list) % 15 == 0 else int(
        (len(deal_with_list) + 15) / 15)
    adist = {}
    page_num = -1
    for i in range(1, comment_page_cut + 1):
        adist.update({i: order_list[15 * (i - 1):15 * i]})

    for i, j in adist.items():
        for n in range(len(j)):
            if int(deal_with_pk) == j[n].pk:
                page_num = i
    return page_num


def article_list(request):
    article_all_list = Article.objects.all()
    context = {}
    context['articles'] = article_all_list
    return render(request, 'article/article_list.html', context)


def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    article_content_type = ContentType.objects.get_for_model(article)
    user = request.user
    article_list = ArticleDetail.objects.filter(content_type=article_content_type, object_id=article.pk)
    context = {}
    # 从消息进入
    score_pk = request.GET.get('score_pk', '')
    if score_pk != '':
        get_score_content_type = ContentType.objects.get_for_model(Article)
        if ScoreRecord.objects.filter(
                content_type=get_score_content_type,
                object_id=article_pk).exists():
            get_score_list = ScoreRecord.objects.filter(
                content_type=get_score_content_type,
                object_id=article_pk)
            page_num = score_from_notification_into(score_pk, get_score_list)
        if page_num != -1:
            return redirect(request.path + '?page=' + str(page_num) + '#scored_' + score_pk)
    # 获取课程是否参加的状态
    if user.is_authenticated:
        if ParticipateRecord.objects.filter(
                content_type=article_content_type, object_id=article.pk, user=user).exists():
            context['is_participate'] = ParticipateRecord.objects.get(
                content_type=article_content_type, object_id=article.pk, user=user).participate
        else:
            context['is_participate'] = None
    # # 获取课程打分人数及平均分
    if ScoreAverage.objects.filter(content_type=article_content_type, object_id=article.pk).exists():
        context['score_avg'] = ScoreAverage.objects.get(
            content_type=article_content_type, object_id=article.pk).average
        context['score_count'] = ScoreAverage.objects.get(
            content_type=article_content_type, object_id=article.pk).count
    else:
        context['score_avg'] = 0
        context['score_count'] = 0
    # 推荐
    recommends = Article.objects.\
        filter(article_type=article.article_type).\
        exclude(pk=article.pk).order_by('?')[:8]
    context['article'] = article
    context['article_list'] = article_list
    context['recommends'] = recommends
    return render(request, 'article/article_detail.html', context)


def article_text(request, article_text_pk):
    context = {}
    user = request.user
    article_id = get_object_or_404(ArticleDetail, pk=article_text_pk).object_id
    article_text = get_object_or_404(ArticleDetail, pk=article_text_pk)
    content_type = ContentType.objects.get_for_model(Article)
    # 入口为消息时
    comment_pk = request.GET.get('comment_pk', '')
    if comment_pk != '':
        get_comment_content_type = ContentType.objects.get_for_model(ArticleDetail)
        if Comment.objects.filter(
                content_type=get_comment_content_type,
                object_id=article_text_pk, parent=None).exists():
            get_comment_list = Comment.objects.filter(
                content_type=get_comment_content_type,
                object_id=article_text_pk,
                parent=None)
            page_num = comment_like_from_notification_into(comment_pk, get_comment_list)
        if page_num != -1:
            return redirect(request.path + '?page=' + str(page_num) + '#comment_' + comment_pk)

    # 是否参加
    if user.is_authenticated:
        if ParticipateRecord.objects.filter(
                content_type=content_type, object_id=article_id, user=user).exists():
            context['is_participate'] = ParticipateRecord.objects.get(
                content_type=content_type, object_id=article_id, user=user).participate
        else:
            context['is_participate'] = None
        if ParticipateRecord.objects.filter(content_type=content_type,
                                            object_id=article_id,
                                            user=user,
                                            participate=True).exists() or article_text.num < 3:
            context['previous_article'] = ArticleDetail.objects.filter(
                content_type=content_type, object_id=article_text.object_id,
                created_time__lt=article_text.created_time).last()
            context['next_article'] = ArticleDetail.objects.filter(
                content_type=content_type, object_id=article_text.object_id,
                created_time__gt=article_text.created_time).first()
            context['article_text'] = article_text
    else:
        return redirect(reverse('home'))
    return render(request, 'article/article_text.html', context)


@login_required
def editor_course(request, add_course_pk=-1):
    from_url = request.GET.get('from', reverse('home'))
    context = {}
    if add_course_pk == -1:
        context['title'] = '创建新课程'
        if request.method == 'POST':
            form = EditorCourseForm(request.POST, request.FILES)
            if form.is_valid():
                if form.cleaned_data['icon'] is not None:
                    new_article = Article.objects.create(
                        title=form.cleaned_data['title'],
                        icon=form.cleaned_data['icon'],
                        article_type=form.cleaned_data['article_type'],
                        grade=form.cleaned_data['grade'],
                        content=form.cleaned_data['content'],
                        author=request.user,
                        introduction=form.cleaned_data['introduction']
                    )
                else:
                    new_article = Article.objects.create(
                        title=form.cleaned_data['title'],
                        article_type=form.cleaned_data['article_type'],
                        grade=form.cleaned_data['grade'],
                        content=form.cleaned_data['content'],
                        author=request.user,
                        introduction=form.cleaned_data['introduction']
                    )
                new_article.save()
                return redirect(from_url)
        else:
            form = EditorCourseForm()
    else:
        context['title'] = '编辑课程'
        if request.method == 'POST':
            form = EditorCourseForm(request.POST, request.FILES)
            if form.is_valid():
                course = Article.objects.get(pk=add_course_pk)
                course.title = form.cleaned_data['title']
                if form.cleaned_data['icon'] is not None:
                    course.icon = form.cleaned_data['icon']
                course.article_type = form.cleaned_data['article_type']
                course.grade = form.cleaned_data['grade']
                course.content = form.cleaned_data['content']
                course.author = request.user
                course.introduction = form.cleaned_data['introduction']
                course.save()
                return redirect(from_url)
        else:
            if Article.objects.filter(pk=add_course_pk).exists():
                course = Article.objects.get(pk=add_course_pk)
                form = EditorCourseForm(
                    initial={
                        'title': course.title,
                        'article_type': course.article_type,
                        'grade': course.grade,
                        'content': course.content,
                        'introduction': course.introduction
                    }
                )
    context['form'] = form
    return render(request, 'article/add_course.html', context)


@login_required
def about_course(request, course_pk):
    course = get_object_or_404(Article, pk=course_pk)
    if request.user == course.author or request.user.get_user_type() != True:
        if ArticleDetail.objects.filter(object_id=course_pk).exists():
            lessons = ArticleDetail.objects.filter(object_id=course_pk)
        else:
            lessons = None
        context = {}
        context['course'] = course
        context['lessons'] = lessons
    else:
        return redirect(reverse('home'))
    return render(request, 'article/editor_course.html', context)


@login_required
def editor_lesson(request, lesson_pk=-1):
    context = {}
    course_pk = request.GET.get('course_pk', -1)
    course = get_object_or_404(Article, pk=course_pk)
    if request.user != course.author or request.user.get_user_type() != True:
        return redirect(reverse('home'))
    from_url = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = EditorLessonForm(request.POST)
        if form.is_valid():
            if lesson_pk == -1:
                content_type = ContentType.objects.get_for_model(Article)
                new_lesson = ArticleDetail.objects.create(
                    content_type=content_type,
                    object_id=course_pk,
                    num=form.cleaned_data['num'],
                    title=form.cleaned_data['title'],
                    text=form.cleaned_data['text']
                )
                new_lesson.save()
                return redirect(from_url)
            else:
                lesson = get_object_or_404(ArticleDetail, pk=lesson_pk)
                lesson.num = form.cleaned_data['num']
                lesson.title = form.cleaned_data['title']
                lesson.text = form.cleaned_data['text']
                lesson.save()
                return redirect(from_url)
    else:
        if lesson_pk == -1:
            if ArticleDetail.objects.filter(object_id=course_pk).exists():
                num = ArticleDetail.objects.filter(object_id=course_pk).count() + 1
            else:
                num = 1
            form = EditorLessonForm(
                initial={
                    'num': num
                }
            )
            context['title'] = '新建课时'
        else:
            lesson = get_object_or_404(ArticleDetail, pk=lesson_pk)
            form = EditorLessonForm(initial={
                'num': lesson.num,
                'title': lesson.title,
                'text': lesson.text
            })
            context['title'] = '编辑课时'
    context['form'] = form
    return render(request, 'article/editor_lesson.html', context)