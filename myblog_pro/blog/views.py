from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from blog.models import Banner, Type, Article, Tag, Link, User


def test(request):
    return render(request, 'blog/test.html')


def get_common_result():
    """此方法用于获取 自定义导航条、特别推荐文章、推荐文章、点击次数最多文章、标签云、友情链接"""
    # 获取自定义导航条设置
    main_menus = Type.objects.filter(parent__isnull=True)
    # 获取特别推荐文章 5篇
    special_recommends = Article.objects.filter(is_delete=False, is_recommend=True, cover__isnull=False).order_by('-create_time')[:5]
    # 获取推荐文章 5篇
    recommends = Article.objects.filter(is_delete=False, is_recommend=True).order_by('-create_time')[:5]
    # 获取点击次数最多的5篇文章
    most_views = Article.objects.filter(is_delete=False).order_by('-view_times')[:5]
    # 获取标签
    tags = Tag.objects.filter(is_use=True).order_by('-create_time')
    # 获取友情链接
    links = Link.objects.filter(is_delete=False)
    return main_menus, special_recommends, recommends, most_views, tags, links


def index(request):
    """首页"""
    if request.method == 'GET':
        # 获取banner滚动图
        banners = Banner.objects.filter(is_delete=False).order_by('-create_time')
        # 获取文章 20篇
        articles = Article.objects.filter(is_delete=False).order_by('-create_time')[:30]

        main_menus, special_recommends, recommends, most_views, tags, links = get_common_result()

        context = {
            'title': '首页 | Alex的个人博客',
            'main_menus': main_menus,
            'banners': banners,
            'articles': articles,
            'banner_recommends': special_recommends[:2],
            'special_recommends': special_recommends[2:],
            'recommends': recommends,
            'most_views': most_views,
            'tags': tags,
            'links': links
        }
        return render(request, 'blog/index.html', context=context)


def about(request):
    """关于我"""
    if request.method == 'GET':
        user = User.objects.first()
        main_menus, special_recommends, recommends, most_views, tags, links = get_common_result()
        context = {
            'title': '关于我 | Alex的个人博客',
            'user': user,
            'main_menus': main_menus
        }
        return render(request, 'blog/about.html', context=context)


def time_axis(request):
    """时间轴"""
    if request.method == 'GET':
        page_now = request.GET.get('pn', 1)
        page_size = 30
        articles = Article.objects.all().order_by('-create_time')
        paginator = Paginator(articles, page_size)
        pages = paginator.page(int(page_now))

        main_menus, special_recommends, recommends, most_views, tags, links = get_common_result()

        context = {
            'title': '时间轴 | Alex的个人博客',
            'main_menus': main_menus,
            'page_articles': pages,
            'special_recommends': special_recommends,
            'recommends': recommends,
            'most_views': most_views,
            'tags': tags,
            'links': links
        }
        return render(request, 'blog/time.html', context=context)


def art_list(request, type_id):
    """文章列表"""
    if request.method == 'GET':
        page_now = request.GET.get('pn', 1)
        page_size = 30
        art_type = Type.objects.filter(type_id=type_id).first()
        if art_type.parent:
            articles = Article.objects.filter(type=art_type, is_delete=False)
        else:
            articles = []
            types = art_type.type_set.filter(is_use=True)
            for t in types:
                articles.extend(Article.objects.filter(type=t, is_delete=False))
        paginator = Paginator(articles, page_size)
        pages = paginator.page(int(page_now))

        main_menus, special_recommends, recommends, most_views, tags, links = get_common_result()

        context = {
            'title': '%s列表页 | Alex的个人博客' % art_type.type_name,
            'type': art_type,
            'main_menus': main_menus,
            'page_articles': pages,
            'special_recommends': special_recommends,
            'recommends': recommends,
            'most_views': most_views,
            'tags': tags,
            'links': links
        }

        return render(request, 'blog/list.html', context=context)


def art_info(request, art_id):
    if request.method == 'GET':
        article = Article.objects.filter(id=art_id).first()

        article.view_times += 1
        article.save()

        next_art = Article.objects.filter(id__gt=art_id, is_delete=False).order_by('id').first()
        prev_art = Article.objects.filter(id__lt=art_id, is_delete=False).order_by('-id').first()

        random_arts = Article.objects.filter(type=article.type).order_by('?')[:10]

        main_menus, special_recommends, recommends, most_views, tags, links = get_common_result()

        context = {
            'title': '%s | Alex的个人博客' % article.title,
            'article': article,
            'next_art': next_art,
            'prev_art': prev_art,
            'random_arts': random_arts,
            'main_menus': main_menus,
            'special_recommends': special_recommends,
            'recommends': recommends,
            'most_views': most_views,
            'tags': tags,
            'links': links
        }

        return render(request, 'blog/info.html', context=context)


def praise(request):
    if request.method == 'POST':
        try:
            art_id = request.POST.get('art_id')
            article = Article.objects.filter(id=art_id).first()
            article.praise_times += 1
            article.save()
            data = {
                'code': 200,
                'msg': '操作成功',
                'praise_times': article.praise_times
            }
        except BaseException as e:
            print(e)
            data = {
                'code': 400,
                'msg': '操作失败'
            }
        return JsonResponse(data)


def message(request):
    pass


def search(request):
    """搜索"""
    if request.method == 'GET':
        page_now = request.GET.get('pn', 1)
        page_size = 30
        search_key = request.GET.get('kw')
        articles = Article.objects.filter(title__icontains=search_key)
        paginator = Paginator(articles, page_size)
        pages = paginator.page(int(page_now))

        main_menus, special_recommends, recommends, most_views, tags, links = get_common_result()

        context = {
            'title': '搜索‘%s’ | Alex的个人博客' % search_key,
            'key': search_key,
            'page_articles': pages,
            'main_menus': main_menus,
            'special_recommends': special_recommends,
            'recommends': recommends,
            'most_views': most_views,
            'tags': tags,
            'links': links
        }

        return render(request, 'blog/search.html', context=context)


def tag_arts(request, tag_id):
    if request.method == 'GET':
        page_now = request.GET.get('pn', 1)
        page_size = 30
        tag = Tag.objects.filter(tag_id=tag_id).first()
        articletags = tag.articletags_set.all()
        paginator = Paginator(articletags, page_size)
        pages = paginator.page(int(page_now))

        main_menus, special_recommends, recommends, most_views, tags, links = get_common_result()

        context = {
            'title': '标签：%s | Alex的个人博客' % tag.tag_name,
            'tag': tag,
            'page_articletags': pages,
            'main_menus': main_menus,
            'special_recommends': special_recommends,
            'recommends': recommends,
            'most_views': most_views,
            'tags': tags,
            'links': links
        }

        return render(request, 'blog/tag_arts.html', context=context)
