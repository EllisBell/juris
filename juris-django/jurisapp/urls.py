from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^acordao/(?P<acordao_id>[0-9]+)/$', views.acordao, name='acordao'),
]