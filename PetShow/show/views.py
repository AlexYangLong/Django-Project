from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from show import status_code
from show.models import Article, Type, Admin, Role, User, Baike, Question, Topic


def page_not_found(request):
    return render(request, '404.html')


def permission_denied(request):
    return render(request, '403.html')


def internal_error(request):
    return render(request, '500.html')


def index(request):
    return JsonResponse({'code': 200, 'msg': '请求成功'})
    # return render(request, 'index.html')


def fresh(request, fid='0'):
    if fid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'GET':
        return render(request, 'fresh.html')
    elif request.method == 'POST':
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 10)
        type_ = Type.objects.filter(pk=fid).first()
        if not type_:
            return JsonResponse(status_code.TYPE_NOT_EXISTS)
        try:
            if type_.parent:
                articles = Article.objects.all().filter(t_id=fid).order_by('-create_time')
                count = articles.count()
                paginator = Paginator(articles, page_size)
                pages = paginator.page(int(page_now))
            else:
                ts = [str(t.id) for t in Type.objects.filter(parent_id=fid)]
                articles = Article.objects.all().filter(t_id__in=ts).order_by('-create_time')
                count = articles.count()
                paginator = Paginator(articles, page_size)
                pages = paginator.page(int(page_now))
            res = status_code.SUCCESS
            res['data_list'] = [art.to_dict() for art in pages.object_list]
            res['data_count'] = count
            res['page_now'] = page_now
            res['page_size'] = page_size
            res['page_count'] = pages.paginator.page_range[-1]
            res['has_next'] = pages.has_next()
            res['has_prev'] = pages.has_previous()
            return JsonResponse(res)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


def fresh_detail(request, fid='0', aid='0'):
    if fid == '0' or aid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'GET':
        article = Article.objects.filter(id=aid).first()
        if not article:
            return JsonResponse(status_code.ARTICLE_NOT_EXISTS)
        res = status_code.SUCCESS
        res['data'] = article.to_dict()
        return JsonResponse(res)


def baike(request):
    if request.method == 'GET':
        return render(request, 'baike.html')
    elif request.method == 'POST':
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 20)

        try:
            baikes = Baike.objects.all().order_by('-create_time')
            count = baikes.count()
            paginator = Paginator(baikes, page_size)
            pages = paginator.page(int(page_now))
            res = status_code.SUCCESS
            res['data_list'] = [bk.to_dict() for bk in pages.object_list]
            res['data_count'] = count
            res['page_now'] = page_now
            res['page_size'] = page_size
            res['page_count'] = pages.paginator.page_range[-1]
            res['has_next'] = pages.has_next()
            res['has_prev'] = pages.has_previous()
            return JsonResponse(res)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


def question(request, qid='0'):
    if request.method == 'GET':
        return render(request, 'question.html')
    elif request.method == 'POST':
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 10)

        try:
            if qid == '0':
                questions = Question.objects.all().order_by('-create_time')
                count = questions.count()
                paginator = Paginator(questions, page_size)
                pages = paginator.page(int(page_now))
                res = status_code.SUCCESS
                res['data_list'] = [bk.to_dict() for bk in pages.object_list]
                res['data_count'] = count
                res['page_now'] = page_now
                res['page_size'] = page_size
                res['page_count'] = pages.paginator.page_range[-1]
                res['has_next'] = pages.has_next()
                res['has_prev'] = pages.has_previous()
                return JsonResponse(res)
            else:
                question = Question.objects.filter(id=qid)
                res = status_code.SUCCESS
                res['data'] = question.to_dict()
                return JsonResponse(res)

        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


def topic(request, tid='0'):
    if request.method == 'GET':
        return render(request, 'topic.html')
    elif request.method == 'POST':
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 10)

        try:
            if tid == '0':
                topics = Topic.objects.all().order_by('-create_time')
                count = topics.count()
                paginator = Paginator(topics, page_size)
                pages = paginator.page(int(page_now))
                res = status_code.SUCCESS
                res['data_list'] = [topic.to_dict() for topic in pages.object_list]
                res['data_count'] = count
                res['page_now'] = page_now
                res['page_size'] = page_size
                res['page_count'] = pages.paginator.page_range[-1]
                res['has_next'] = pages.has_next()
                res['has_prev'] = pages.has_previous()
                return JsonResponse(res)
            else:
                topic = Topic.objects.filter(id=tid)
                res = status_code.SUCCESS
                res['data'] = topic.to_dict()
                return JsonResponse(res)

        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)
