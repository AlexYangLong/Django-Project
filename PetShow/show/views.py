import random

from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

from show import status_code
from show.models import Article, Type, Admin, Role, User, Baike, Question, Topic, TopicPic, Pet, PetDoodle, PetComment


def page_not_found(request):
    return render(request, '404.html')


def permission_denied(request):
    return render(request, '403.html')


def internal_error(request):
    return render(request, '500.html')


# def index(request):
#
#     return JsonResponse({'code': 200, 'msg': '请求成功'})
    # return render(request, 'index.html')


def pets(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        type_ = request.GET.get('t', 'tpty')
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 50)

        try:
            pets = Pet.objects.all()
            if type_ == 'yyty':
                pets = pets.filter(t='语音涂鸦').order_by('-create_time')
            elif type_ == 'rqzg':
                pets = pets.order_by('-like_num')
            elif type_ == 'zxmc':
                pets = pets.order_by('-create_time')
            elif type_ == 'tpty':
                pets = pets.filter(t='图片涂鸦').order_by('-create_time')
            count = pets.count()
            paginator = Paginator(pets, page_size)
            pages = paginator.page(int(page_now))
            res = status_code.SUCCESS
            res['data_list'] = [pet.to_dict() for pet in pages.object_list]
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


def pet_detail(request, pid='0'):
    if pid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'GET':
        pet = Pet.objects.filter(id=pid).first()
        if not pet:
            return JsonResponse(status_code.PET_NOT_EXISTS)
        return render(request, 'pet_detail.html', {'pet': pet})


def get_doodle(request, pid='0'):
    if pid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'POST':
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 50)

        try:
            doodles = PetDoodle.objects.filter(pet_id=pid).all().order_by('-create_time')
            count = doodles.count()
            paginator = Paginator(doodles, page_size)
            pages = paginator.page(int(page_now))
            res = status_code.SUCCESS
            res['data_list'] = [doodle.to_dict() for doodle in pages.object_list]
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


def get_comment(request, pid='0'):
    if pid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'POST':
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 20)

        try:
            comments = PetComment.objects.filter(pet_id=pid).all().order_by('-create_time')
            count = comments.count()
            paginator = Paginator(comments, page_size)
            pages = paginator.page(int(page_now))
            res = status_code.SUCCESS
            res['data_list'] = [comment.to_dict() for comment in pages.object_list]
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


def get_hot_list(request):
    if request.method == 'GET':
        try:
            pets = Pet.objects.order_by('-like_num').all()[:10]
            res = status_code.SUCCESS
            res['data_list'] = [pet.to_dict() for pet in pets]
            return JsonResponse(res)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


def get_random_list(request):
    if request.method == 'GET':
        try:
            pets = Pet.objects.all()
            count = pets.count()
            if count > 8:
                pets = random.sample(list(pets), k=8)
            else:
                pets = pets
            res = status_code.SUCCESS
            res['data_list'] = [pet.to_dict() for pet in pets]
            return JsonResponse(res)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


def fresh_know(request, fid='0'):
    if fid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'GET':
        t = request.GET.get('t')
        if t == 'fresh':
            return render(request, 'fresh.html')
        elif t == 'knowledge':
            return render(request, 'knowledge.html')
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


def fresh_know_detail(request, aid='0'):
    if aid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'GET':
        article = Article.objects.filter(id=aid).first()
        if not article:
            return JsonResponse(status_code.ARTICLE_NOT_EXISTS)
        # res = status_code.SUCCESS
        # res['data'] = article.to_dict()
        # return JsonResponse(res)
        return render(request, 'article.html', {'article': article})


def show_more(request, tid):
    if request.method == 'GET':
        try:
            articles = Article.objects.filter(t_id=tid).all()
            count = articles.count()
            if count > 5:
                arts = random.sample(list(articles), k=5)
            else:
                arts = articles
            res = status_code.SUCCESS
            res['data_list'] = [art.to_dict() for art in arts]
            return JsonResponse(res)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


def baike(request):
    if request.method == 'GET':
        return render(request, 'baike.html')
    elif request.method == 'POST':
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 20)

        try:
            baikes = Baike.objects.all().order_by('create_time')
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


def baike_detail(request, bid='0'):
    if bid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'GET':
        baike = Baike.objects.filter(id=bid).first()
        if not baike:
            return JsonResponse(status_code.BAIKE_NOT_EXISTS)
        # res = status_code.SUCCESS
        # res['data'] = baike.to_dict()
        # return JsonResponse(res)
        return render(request, 'baike_detail.html', {'baike': baike})


def question(request):
    if request.method == 'GET':
        return render(request, 'question.html')
    elif request.method == 'POST':
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 10)

        try:
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
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


def question_detail(request, qid='0'):
    if qid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'GET':
        ques = Question.objects.filter(id=qid).first()
        if not ques:
            return JsonResponse(status_code.BAIKE_NOT_EXISTS)
        # res = status_code.SUCCESS
        # res['data'] = ques.to_dict()
        # return JsonResponse(res)
        return render(request, 'question_detail.html', {'question': ques})


def topic(request):
    if request.method == 'GET':
        return render(request, 'topic.html')
    elif request.method == 'POST':
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 10)

        try:
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
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


def topic_detail(request, tid='0'):
    if tid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'GET':
        top = Topic.objects.filter(id=tid).first()
        if not top:
            return JsonResponse(status_code.TOPIC_NOT_EXISTS)
        return render(request, 'topic_detail.html', {'topic': top})
    elif request.method == 'POST':
        top = Topic.objects.filter(id=tid).first()
        if not top:
            return JsonResponse(status_code.TOPIC_NOT_EXISTS)
        res = status_code.SUCCESS
        res['data'] = top.to_full_dict()
        return JsonResponse(res)


def topic_imgs(request, tid='0'):
    if tid == '0':
        return JsonResponse(status_code.REQUEST_PARAM_ERROR)
    if request.method == 'POST':
        page_now = request.GET.get('pn', 1)
        page_size = request.GET.get('ps', 20)

        try:
            pics = TopicPic.objects.filter(topic_id=tid).all().order_by('-create_time')
            count = pics.count()
            paginator = Paginator(pics, page_size)
            pages = paginator.page(int(page_now))
            res = status_code.SUCCESS
            res['data_list'] = [pic.to_dict() for pic in pages.object_list]
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
