from django.conf.urls import url, handler403, handler400, handler500

from show import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),

    url(r'^fresh/(\d+)/$', views.fresh, name='fresh'),
    url(r'^fresh/(\d+)/(\d+).html$', views.fresh_detail),

    url(r'^baike/(\d+)/$', views.baike, name='baike'),

    url(r'^question/(\d+)/$', views.question, name='question'),

    url(r'^topic/(\d+)/$', views.topic, name='topic'),

]

from show.views import *
handler403 = permission_denied
handler400 = page_not_found
handler500 = internal_error
