from functools import wraps

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Create your views here.
from bms import status_code
from bms.models import Admin, LoginRecord, Authority, Role


def login_required(func):
    @wraps(func)
    def is_login(*args, **kwargs):
        if not args[0].session.get('adid'):
            return redirect('/bms/login/')
        return func(*args, **kwargs)
    return is_login


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        admin = Admin.objects.filter(username=username, password=password).first()

        if admin:
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            lc = LoginRecord()
            lc.login_ip = ip
            lc.admin = admin
            lc.save()
            admin.to_dict()
            request.session['adid'] = admin.id
            request.session.set_expiry(20 * 60)  # 设置session过期时间

            return JsonResponse(status_code.SUCCESS)
        return JsonResponse(status_code.LOGIN_USERNAME_OR_PASSWORD_ERROR)


@login_required
def logout(request):
    del request.session['adid']
    return redirect('/bms/login/')


@login_required
def get_admin_info(request):
    if request.method == 'GET':
        admin = Admin.objects.filter(id=request.session.get('adid')).first()
        if not admin:
            return JsonResponse(status_code.ADMIN_NOT_EXISTS)
        res = status_code.SUCCESS
        res['data'] = admin.to_dict()
        return JsonResponse(res)


@login_required
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


@login_required
def get_menu_by_ad(request):
    if request.method == 'GET':
        adid = request.session.get('adid')
        admin = Admin.objects.filter(id=adid).first()
        auths = admin.role.auths.all()
        res = status_code.SUCCESS
        res['menu_list'] = []
        for auth in auths:
            if not auth.parent_id:
                data = dict(menu=auth.name)
                data['submenu'] = []
                for a in auths:
                    if a.parent_id == auth.id:
                        sub_data = dict(menu=a.name, url=a.url)
                        data['submenu'].append(sub_data)
                res['menu_list'].append(data)
        return JsonResponse(res)


@login_required
def auth_list(request):
    if request.method == 'GET':
        return render(request, 'admin/auth_list.html')


@login_required
def get_auth_list(request):
    if request.method == 'GET':
        pn = int(request.GET.get('pn', 1))
        ps = 10
        sk = request.GET.get('sk')
        if not sk:
            try:
                data_count = Authority.objects.count()
                auths = Authority.objects.all().order_by('-id')
                paginator = Paginator(auths, ps)
                pages = paginator.page(pn)
                res = status_code.SUCCESS
                res['data_count'] = data_count
                res['data_list'] = [auth.to_dict() for auth in pages.object_list]
                res['pn'] = pn
                res['ps'] = ps
                res['page_count'] = pages.paginator.page_range[-1]
                res['has_next'] = pages.has_next()
                res['has_prev'] = pages.has_previous()
                return JsonResponse(res)
            except BaseException as e:
                print(e)
                return JsonResponse(status_code.DATABASE_ERROR)

        try:
            data_count = Authority.objects.filter(name__icontains=sk).count()
            auths = Authority.objects.filter(name__icontains=sk).order_by('-id')
            paginator = Paginator(auths, ps)
            pages = paginator.page(pn)
            res = status_code.SUCCESS
            res['data_count'] = data_count
            res['data_list'] = [auth.to_dict() for auth in pages.object_list]
            res['pn'] = pn
            res['ps'] = ps
            res['page_count'] = pages.paginator.page_range[0]
            res['has_next'] = pages.has_next()
            res['has_prev'] = pages.has_previous()
            return JsonResponse(res)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


@login_required
def get_auth_by_id(request, aid):
    if request.method == 'GET':
        auth = Authority.objects.filter(id=aid).first()
        res = status_code.SUCCESS
        res['data'] = auth.to_dict()
        return JsonResponse(res)


@login_required
def get_auths_by_fj(request):
    auths = Authority.objects.filter(parent_id=None)
    res = status_code.SUCCESS
    res['data_list'] = [auth.to_parent_dict() for auth in auths]
    return JsonResponse(res)


@login_required
def get_auths(request):
    if request.method == 'GET':
        auths = Authority.objects.all()
        res = status_code.SUCCESS
        res['data_list'] = [auth.to_dict() for auth in auths]
        return JsonResponse(res)


@login_required
def auth_addoredit(request):
    if request.method == 'GET':
        return render(request, 'admin/auth_addoredit.html')
    elif request.method == 'POST':
        auth_id = request.POST.get('auth_id')
        auth_name = request.POST.get('auth_name')
        auth_url = request.POST.get('auth_url')
        parent_id = request.POST.get('parent')
        if not auth_id:
            try:
                auth = Authority.objects.filter(name=auth_name).first()
                if auth:
                    return JsonResponse(status_code.AUTH_ALREADY_EXISTS)
                auth = Authority()
                auth.name = auth_name
                auth.url = auth_url
                auth.parent_id = parent_id
                auth.admin_id = request.session.get('adid')
                auth.save()
                return JsonResponse(status_code.SUCCESS)
            except BaseException as e:
                print(e)
                return JsonResponse(status_code.DATABASE_ERROR)
        try:
            auth = Authority.objects.filter(id=auth_id).first()
            if not auth:
                return JsonResponse(status_code.AUTH_NOT_EXISTS)
            auth.name = auth_name
            auth.url = auth_url
            auth.parent_id = parent_id
            auth.save()
            return JsonResponse(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


@login_required
def auth_del(request):
    if request.method == 'POST':
        aid = request.POST.get('aid')
        try:
            auth = Authority.objects.filter(id=aid).first()
            if not auth:
                return JsonResponse(status_code.AUTH_NOT_EXISTS)
            auth.delete()
            return JsonResponse(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


@login_required
def role_list(request):
    if request.method == 'GET':
        return render(request, 'admin/role_list.html')


@login_required
def get_role_list(request):
    if request.method == 'GET':
        pn = int(request.GET.get('pn', 1))
        ps = 10
        try:
            data_count = Role.objects.count()
            roles = Role.objects.all().order_by('-id')
            paginator = Paginator(roles, ps)
            pages = paginator.page(pn)
            res = status_code.SUCCESS
            res['data_count'] = data_count
            res['data_list'] = [role.to_full_dict() for role in pages.object_list]
            res['pn'] = pn
            res['ps'] = ps
            res['page_count'] = pages.paginator.page_range[-1]
            res['has_next'] = pages.has_next()
            res['has_prev'] = pages.has_previous()
            return JsonResponse(res)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


@login_required
def get_roles(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        res = status_code.SUCCESS
        res['data_list'] = [role.to_dict() for role in roles]
        return JsonResponse(res)


@login_required
def get_role_by_id(request, rid):
    if request.method == 'GET':
        role = Role.objects.filter(id=rid).first()
        res = status_code.SUCCESS
        res['data'] = role.to_auth_info_dict()
        return JsonResponse(res)


@login_required
def role_addoredit(request):
    if request.method == 'GET':
        return render(request, 'admin/role_addoredit.html')
    elif request.method == 'POST':
        role_id = request.POST.get('role_id')
        role_name = request.POST.get('role_name')
        description = request.POST.get('description')
        aids = [int(i) for i in request.POST.get('aids').split(',')[:-1]]
        if not role_id:
            try:
                role = Role.objects.filter(name=role_name).first()
                if role:
                    return JsonResponse(status_code.ROLE_ALREADY_EXISTS)
                # 在新增修改角色时 使用事务，使用上下文手动提交
                with transaction.atomic():
                    auths = Authority.objects.filter(id__in=aids).all()
                    role = Role()
                    role.name = role_name
                    role.description = description
                    role.aid = request.session.get('adid')
                    role.save()
                    role.auths = auths
                    return JsonResponse(status_code.SUCCESS)
            except BaseException as e:
                print(e)
                return JsonResponse(status_code.DATABASE_ERROR)
        try:
            role = Role.objects.filter(id=role_id).first()
            if not role:
                return JsonResponse(status_code.ROLE_NOT_EXISTS)
            # 在新增修改角色时 使用事务，使用上下文手动提交
            with transaction.atomic():
                auths = Authority.objects.filter(id__in=aids).all()
                role.name = role_name
                role.description = description
                role.auths = auths
                role.save()
                return JsonResponse(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


@login_required
def role_del(request):
    if request.method == 'POST':
        rid = request.POST.get('rid')
        try:
            role = Role.objects.filter(id=rid).first()
            if not role:
                return JsonResponse(status_code.ROLE_NOT_EXISTS)
            role.delete()
            return JsonResponse(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


@login_required
def admin_list(request):
    if request.method == 'GET':
        return render(request, 'admin/admin_list.html')


@login_required
def get_admin_list(request):
    if request.method == 'GET':
        pn = int(request.GET.get('pn', 1))
        ps = 10
        sk = request.GET.get('sk')
        if not sk:
            try:
                data_count = Admin.objects.count()
                admins = Admin.objects.all().order_by('-id')
                paginator = Paginator(admins, ps)
                pages = paginator.page(pn)
                res = status_code.SUCCESS
                res['data_count'] = data_count
                res['data_list'] = [admin.to_dict() for admin in pages.object_list]
                res['pn'] = pn
                res['ps'] = ps
                res['page_count'] = pages.paginator.page_range[-1]
                res['has_next'] = pages.has_next()
                res['has_prev'] = pages.has_previous()
                return JsonResponse(res)
            except BaseException as e:
                print(e)
                return JsonResponse(status_code.DATABASE_ERROR)

        try:
            data_count = Admin.objects.filter(Q(name__icontains=sk) | Q(username__icontains=sk)).count()
            admins = Admin.objects.filter(Q(name__icontains=sk) | Q(username__icontains=sk)).order_by('-id')
            paginator = Paginator(admins, ps)
            pages = paginator.page(pn)
            res = status_code.SUCCESS
            res['data_count'] = data_count
            res['data_list'] = [admin.to_dict() for admin in pages.object_list]
            res['pn'] = pn
            res['ps'] = ps
            res['page_count'] = pages.paginator.page_range[0]
            res['has_next'] = pages.has_next()
            res['has_prev'] = pages.has_previous()
            return JsonResponse(res)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


@login_required
def admin_addoredit(request):
    if request.method == 'GET':
        return render(request, 'admin/admin_addoredit.html')
    elif request.method == 'POST':
        adid = request.POST.get('admin_id')
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        role = request.POST.get('role')
        if not adid:
            try:
                admin = Admin.objects.filter(username=username).first()
                if admin:
                    return JsonResponse(status_code.ADMIN_ALREADY_EXISTS)
                admin = Admin()
                admin.username = username
                admin.name = name
                admin.password = password
                admin.gender = int(gender)
                admin.phone = phone
                admin.email = email
                admin.role_id = role
                admin.save()
                return JsonResponse(status_code.SUCCESS)
            except BaseException as e:
                print(e)
                return JsonResponse(status_code.DATABASE_ERROR)
        try:
            admin = Admin.objects.filter(id=adid).first()
            if not admin:
                return JsonResponse(status_code.ADMIN_NOT_EXISTS)
            admin.username = username
            admin.name = name
            admin.password = password
            admin.gender = int(gender)
            admin.phone = phone
            admin.email = email
            admin.role_id = role
            admin.save()
            return JsonResponse(status_code.SUCCESS)
        except BaseException as e:
            print(e)
            return JsonResponse(status_code.DATABASE_ERROR)


@ login_required
def get_admin_by_id(request, adid):
    if request.method == 'GET':
        admin = Admin.objects.filter(id=adid).first()
        res = status_code.SUCCESS
        res['data'] = admin.to_dict()
        return JsonResponse(res)
