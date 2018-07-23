from django.conf.urls import url, handler403, handler400, handler500

from show import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),

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

]

from show.views import *
handler403 = permission_denied
handler400 = page_not_found
handler500 = internal_error
