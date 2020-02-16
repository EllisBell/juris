from django.conf.urls import url
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_relevant/$', views.search_relevant, name='search_relevant'),
    url(r'^search_recent/$', views.search_recent, name='search_recent'),
    url(r'^save_search/$', views.save_search, name='save_search'),
    url(r'^suggest_processo/$', views.suggest_processo, name='suggest_processo'),
    url(r'^acordao/(?P<acordao_id>[0-9]+)/$', views.acordao, name='acordao'),
    url(r'^acordao/(?P<acordao_id>[0-9]+)/pdf/$', views.acordao_pdf, name='acordao_pdf'),
    url(r'^recentes/$', views.recent_acordaos, name='recent_acordaos'),
    url(r'^termos', TemplateView.as_view(template_name='jurisapp/termos.html'), name='termos'),
    url(r'^sobre', TemplateView.as_view(template_name='jurisapp/sobre.html'), name='sobre'),
]