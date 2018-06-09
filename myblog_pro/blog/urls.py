from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^test/', views.test, name='test'),

    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^time_axis/', views.time_axis, name='time_axis'),
    url(r'^message/', views.message, name='message'),

    url(r'^art_list/(?P<type_id>\d+)/', views.art_list, name='art_list'),
    url(r'^art_info/(?P<art_id>\d+)/', views.art_info, name='art_info'),
    url(r'^art_info/praise/', views.praise, name='praise'),

    url(r'^search/', views.search, name='search'),

    url(r'^tag_arts/(?P<tag_id>\d+)/', views.tag_arts, name='tag_arts'),
]
