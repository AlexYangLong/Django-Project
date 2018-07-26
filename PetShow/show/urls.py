from django.conf.urls import url, handler403, handler400, handler500

from show import views

urlpatterns = [
    url(r'^$', views.pets, name='index'),
    url(r'^index/$', views.pets, name='index'),

    url(r'^pets/$', views.pets, name='pets'),
    url(r'^pets/(\d+).html$', views.pet_detail),
    url(r'^get_doodle/(\d+)/$', views.get_doodle),
    url(r'^get_comment/(\d+)/$', views.get_comment),
    url(r'^get_hot_list/$', views.get_hot_list),
    url(r'^get_random_list/$', views.get_random_list),

    url(r'^fresh/(\d+)/$', views.fresh_know, name='fresh'),
    url(r'^fresh/(\d+).html$', views.fresh_know_detail),

    url(r'^knowledge/(\d+)/$', views.fresh_know, name='knowledge'),
    url(r'^knowledge/(\d+).html$', views.fresh_know_detail),

    url(r'^show_more/(\d+)/$', views.show_more),

    url(r'^baike/$', views.baike, name='baike'),
    url(r'^baike/(\d+).html$', views.baike_detail),

    url(r'^question/$', views.question, name='question'),
    url(r'^question/(\d+).html$', views.question_detail),

    url(r'^topic/$', views.topic, name='topic'),
    url(r'^topic/(\d+).html$', views.topic_detail),
    url(r'^topic_imgs/(\d+)/$', views.topic_imgs),

]

from show.views import *
handler403 = permission_denied
handler400 = page_not_found
handler500 = internal_error
