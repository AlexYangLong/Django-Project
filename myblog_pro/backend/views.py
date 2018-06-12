from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from blog.models import User, Article, Type, Tag, Link
from utils.StatusCodeEnum import StatusCode


def login(request):
    """登录"""
    if request.method == 'GET':
        return render(request, 'backend/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not all(username, password):
        data = {
            'code': StatusCode.PARAMS_NOT_COMPLETE,
            'msg': '参数不完整'
        }
        return JsonResponse(data)

    user = User.objects.filter(username=username).first()
    if user:
        if check_password(password, user.password):
            data = {
                'code': StatusCode.SUCCESS,
                'msg': '验证成功'
            }
        else:
            data = {
                'code': StatusCode.PASSWORD_ERROR,
                'msg': '密码错误'
            }
    else:
        data = {
            'code': StatusCode.USERNAME_NOT_EXISTS,
            'msg': '用户名不存在'
        }
    return JsonResponse(data=data)


def change_password(request):
    """修改密码"""
    if request.method == 'POST':
        uid = request.POST.get('uid')
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')
        user = User.objects.filter(user_id=uid).first()
        if not user:
            data = {
                'code': StatusCode.USERNAME_NOT_EXISTS,
                'msg': '用户不存在'
            }
            return JsonResponse(data)

        if not check_password(old_pwd, user.password):
            data = {
                'code': StatusCode.PASSWORD_ERROR,
                'msg': '原密码错误'
            }
            return JsonResponse(data)
        user.password = make_password(new_pwd)
        user.save()
        data = {
            'code': StatusCode.SUCCESS,
            'msg': '操作成功'
        }
        return JsonResponse(data)


def user_list(request):
    """用户列表"""
    if request.method == 'GET':
        page_now = request.GET.get('pn', 1)
        page_size = 15
        users = User.objects.filter(is_delete=False).order_by('-create_time')
        paginator = Paginator(users, page_size)
        page_users = paginator.page(int(page_now))

        data = {
            'code': StatusCode.SUCCESS,
            'msg': '操作成功',
            'datalist': page_users
        }

        return JsonResponse(data)


def create_user(request):
    """创建用户"""
    if request.method == 'GET':
        return render(request, 'backend/create_user.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    sex = request.POST.get('sex')
    icon = request.FILES.get('icon')
    brief = request.POST.get('brief')

    if not all(username, password, email, sex):
        data = {
            'code': StatusCode.PARAMS_NOT_COMPLETE,
            'msg': '参数不完整'
        }
        return JsonResponse(data)
    user = User.objects.filter(username=username).first()
    if user:
        data = {
            'code': StatusCode.USERNAME_EXISTS,
            'msg': '用户已存在'
        }
        return JsonResponse(data)

    user = User.objects.create(username=username,
                               password=make_password(password),
                               email=email,
                               sex=sex,
                               icon=icon,
                               brief=brief)
    data = {
        'code': StatusCode.SUCCESS,
        'msg': '操作成功',
        'data_obj': user
    }
    return JsonResponse(data)


def update_user(request):
    """修改用户"""
    pass


def delete_user(request):
    """删除用户"""
    if request.method == 'POST':
        uid = request.POST.get('uid')
        user = User.objects.filter(user_id=uid).first()
        user.is_delete = True
        user.save()
        data = {
            'code': StatusCode.SUCCESS,
            'msg': '操作成功'
        }
        return JsonResponse(data)


def article_list(request):
    """文章列表"""
    if request.method == 'GET':
        page_now = request.GET.get('pn', 1)
        page_size = 15
        articles = Article.objects.filter(is_delete=False).order_by('-create_time')
        paginator = Paginator(articles, page_size)
        page_articles = paginator.page(int(page_now))

        data = {
            'code': StatusCode.SUCCESS,
            'msg': '操作成功',
            'datalist': page_articles
        }

        return JsonResponse(data)


def create_article(request):
    """新增文章"""
    if request.method == 'GET':
        return render(request, 'backend/article_addoredit.html')

    title = request.POST.get('title')
    brief = request.POST.get('brief')
    content = request.POST.get('content')
    cover = request.FILES.get('cover')
    is_recommend = request.POST.get('is_recommend')
    type_id = request.POST.get('type')
    author = request.POST.get('author')

    if not all(title, brief, content,is_recommend, type_id, author):
        data = {
            'code': StatusCode.PARAMS_NOT_COMPLETE,
            'msg': '参数不完整'
        }
        return JsonResponse(data)

    art = Article.objects.create(title=title,
                                 brief=brief,
                                 content=content,
                                 cover=cover,
                                 is_recommend=is_recommend,
                                 type_id=type_id,
                                 author_id=author)
    data = {
        'code': StatusCode.SUCCESS,
        'msg': '操作成功',
        'data_obj': art
    }
    return JsonResponse(data)


def update_article(request):
    """修改文章"""
    pass


def delete_article(request):
    """删除文章"""
    if request.method == 'POST':
        aid = request.POST.get('aid')
        art = Article.objects.filter(id=aid).first()
        art.is_delete = True
        art.save()
        data = {
            'code': StatusCode.SUCCESS,
            'mag': '操作成功'
        }
        return JsonResponse(data)


def article_recommend(request):
    """修改文章推荐"""
    if request.method == 'POST':
        aid = request.POST.get('aid')
        article = Article.objects.filter(id=aid).first()
        article.is_recommend = not article.is_recommend
        article.save()
        data = {
            'code': StatusCode.SUCCESS,
            'mag': '操作成功'
        }
        return JsonResponse(data)


def type_list(request):
    """文章类型列表"""
    if request.method == 'GET':
        page_now = request.GET.get('pn', 1)
        page_size = 15
        types = Type.objects.all().order_by('-create_time')
        paginator = Paginator(types, page_size)
        page_types = paginator.page(int(page_now))

        data = {
            'code': StatusCode.SUCCESS,
            'msg': '操作成功',
            'datalist': page_types
        }

        return JsonResponse(data)


def create_type(request):
    """新增文章分类"""
    if request.method == 'GET':
        return render(request, 'backend/type_addoredit.html')

    type_name = request.POST.get('type_name')
    parent_id = request.POST.get('parent_id')

    if not all(type_name, parent_id):
        data = {
            'code': StatusCode.PARAMS_NOT_COMPLETE,
            'msg': '参数不完整'
        }
        return JsonResponse(data)

    art_type = Type.objects.filter(type_name=type_name).first()
    if art_type:
        data = {
            'code': StatusCode.TYPE_EXISTS,
            'msg': '类型已存在'
        }
        return JsonResponse(data)

    Type.objects.create(type_name=type_name,
                        parent_id=parent_id)
    data = {
        'code': StatusCode.SUCCESS,
        'msg': '操作成功'
    }
    return JsonResponse(data)


def update_type(request):
    """修改文章分类"""
    pass


def delete_type(request):
    """删除文章分类"""
    if request.method == 'POST':
        type_id = request.POST.get('tid')
        art_type = Type.objects.filter(type_id=type_id).first()
        art_type.is_use = False
        art_type.save()
        data = {
            'code': StatusCode.SUCCESS,
            'msg': '操作成功'
        }
        return JsonResponse(data)


def tag_list(request):
    """标签列表"""
    if request.method == 'GET':
        page_now = request.GET.get('pn', 1)
        page_size = 15
        tags = Tag.objects.all().order_by('-create_time')
        paginator = Paginator(tags, page_size)
        page_tags = paginator.page(int(page_now))

        data = {
            'code': StatusCode.SUCCESS,
            'msg': '操作成功',
            'datalist': page_tags
        }

        return JsonResponse(data)


def create_tag(request):
    """新增标签"""
    if request.method == 'GET':
        return render(request, 'backend/tag_addoredit.html')

    tag_name = request.POST.get('tag_name')
    if not all(tag_name):
        data = {
            'code': StatusCode.PARAMS_NOT_COMPLETE,
            'msg': '参数不完整'
        }
        return JsonResponse(data)

    tag = Tag.objects.filter(tag_name=tag_name).first()
    if tag:
        data = {
            'code': StatusCode.TAG_EXISTS,
            'msg': '标签名已存在'
        }
        return JsonResponse(data)
    Tag.objects.create(tag_name=tag_name)
    data = {
        'code': StatusCode.SUCCESS,
        'msg': '操作成功'
    }
    return JsonResponse(data)


def update_tag(request):
    """修改标签"""
    pass


def delete_tag(request):
    """删除标签"""
    if request.method == 'POST':
        tid = request.POST.get('tid')
        tag = Tag.objects.filter(tag_id=tid).first()
        tag.is_use = False
        tag.save()
        data = {
            'code': StatusCode.SUCCESS,
            'msg': '操作成功'
        }
        return JsonResponse(data)


def link_list(request):
    """友链列表"""
    if request.method == 'GET':
        page_now = request.GET.get('pn', 1)
        page_size = 15
        links = Link.objects.all().order_by('-create_time')
        paginator = Paginator(links, page_size)
        page_links = paginator.page(int(page_now))

        data = {
            'code': StatusCode.SUCCESS,
            'msg': '操作成功',
            'datalist': page_links
        }

        return JsonResponse(data)


def create_link(request):
    """新增链接"""
    if request.method == 'GET':
        return render(request, 'backend/link_addoredit.html')

    link_name = request.POST.get('link_name')
    link_url = request.POST.get('link_url')
    if not all(link_name, link_url):
        data = {
            'code': StatusCode.PARAMS_NOT_COMPLETE,
            'msg': '参数不完整'
        }
        return JsonResponse(data)
    link = Link.objects.filter(link_name=link_name).first()
    if link:
        data = {
            'code': StatusCode.LINK_EXISTS,
            'msg': '链接已存在'
        }
        return JsonResponse(data)
    Link.objects.create(link_name=link_name, link_url=link_url)
    data = {
        'code': StatusCode.SUCCESS,
        'msg': '操作成功'
    }
    return JsonResponse(data)


def update_link(request):
    """修改链接"""
    pass


def delete_link(request):
    """删除链接"""
    if request.method == 'POST':
        lid = request.POST.get('lid')
        link = Link.objects.filter(id=lid).first()
        link.is_delete = True
        link.save()
        data = {
            'code': StatusCode.SUCCESS,
            'msg': '操作成功'
        }
        return JsonResponse(data)
