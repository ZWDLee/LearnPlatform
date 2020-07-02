from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from article.models import Article
from article_statistics.models import IndexWheels
from article_statistics.models import ParticipateCount


def home(request):
    # 轮播图
    wheels = IndexWheels.objects.all()
    context = {}
    context['wheels'] = wheels

    # articles
    article_all_list = Article.objects.all()
    adist = {}
    order_list = []
    for i in range(len(article_all_list)):
      adist.update(
          {article_all_list[i]: ParticipateCount.objects.get(
              object_id=article_all_list[i].pk
          ).participate_num if ParticipateCount.objects.filter(object_id=article_all_list[i].pk) else 0}
      )
    sorted_dist = sorted(adist.items(), key=lambda adist: adist[1], reverse=True)
    for i in range(len(sorted_dist)):
        order_list.append(sorted_dist[i][0])
    article_list_by_cj = Article.objects.filter(grade=0).order_by('?')[:8]
    article_list_by_gj = Article.objects.filter(grade=2).order_by('?')[:8]
    context['articles'] = order_list[:8]
    context['article_list_by_cj'] = article_list_by_cj
    context['article_list_by_gj'] = article_list_by_gj
    return render(request, 'home.html', context)


def search(request):
    words = request.GET.get('wd', '').strip()
    category_wd = request.GET.get('c_wd', '')
    page_num = request.GET.get('page', 1)
    context = {}
    result = []
    if category_wd == '':
        # 分词搜索
        condition = None
        for word in words.split(' '):
            if condition == None:
                condition = Q(title__icontains=word)
            else:
                condition = condition | Q(title__icontains=word)

        if condition is not None:
            result = Article.objects.filter(condition)
        context['words'] = words
    else:
        # 分类搜索
        result = Article.objects.filter(article_type__type_name__icontains=category_wd)
        context['words'] = category_wd
    paginator = Paginator(result, 20)
    page_for_result = paginator.get_page(page_num)

    # 推荐课程
    recommends = Article.objects.order_by('?')[:5]



    context['result_count'] = result.count()
    context['paginator'] = paginator
    context['page_for_result'] = page_for_result
    context['recommends'] = recommends
    return render(request, 'search.html', context)
