from django.conf.urls import url

from bms import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^index/', views.index, name='index'),
    url(r'^get_menu_by_ad/', views.get_menu_by_ad),
    url(r'^get_admin_info', views.get_admin_info),

    url(r'^auths/', views.auth_list, name='auths'),
    url(r'^get_auth_list/', views.get_auth_list),
    url(r'^get_auths/', views.get_auths),
    url(r'^get_auth_by_id/(\d+)/', views.get_auth_by_id),
    url(r'^get_auths_by_fj/', views.get_auths_by_fj),
    url(r'^auth_addoredit/', views.auth_addoredit, name='auth_addoredit'),
    url(r'^auth_del/', views.auth_del, name='auth_del'),

    url(r'^roles/', views.role_list, name='roles'),
    url(r'^get_role_list/', views.get_role_list),
    url(r'^get_roles/', views.get_roles),
    url(r'^get_role_by_id/(\d+)/', views.get_role_by_id),
    url(r'^role_addoredit/', views.role_addoredit, name='role_addoredit'),
    url(r'^role_del/', views.role_del, name='role_del'),

    url(r'^admins/', views.admin_list, name='admins'),
    url(r'^get_admin_list/', views.get_admin_list),
    url(r'^admin_addoredit/', views.admin_addoredit, name='admin_addoredit'),
    url(r'^get_admin_by_id/(\d+)/', views.get_admin_by_id),
]
