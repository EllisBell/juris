from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_relevant/$', views.search_relevant, name='search_relevant'),
    url(r'^search_recent/$', views.search_recent, name='search_recent'),
    url(r'^acordao/(?P<acordao_id>[0-9]+)/$', views.acordao, name='acordao'),
]