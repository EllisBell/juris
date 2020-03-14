from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.urls import path, re_path


urlpatterns = [
    path('', views.index, name='juris_index'),
    re_path('search_relevant/$', views.search_relevant, name='search_relevant'),
    re_path('search_recent/$', views.search_recent, name='search_recent'),    
    re_path('save_search/$', views.save_search, name='save_search'),
    re_path('suggest_processo/$', views.suggest_processo, name='suggest_processo'),
    path('acordao/<int:acordao_id>/', views.acordao, name='acordao'),
    path('acordao/<int:acordao_id>/pdf/', views.acordao_pdf, name='acordao_pdf'),
    path('recentes', views.recent_acordaos, name='recent_acordaos'),
    path('register/', views.register, name='register'), 
    path('login/', auth_views.LoginView.as_view(template_name='jurisapp/registration/login.html'), name='juris_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='juris_logout'),
    path('dossier/', views.dossier_home, name='dossier_home'), 
    path('termos', TemplateView.as_view(template_name='jurisapp/termos.html'), name='termos'),
    path('sobre', TemplateView.as_view(template_name='jurisapp/sobre.html'), name='sobre'),
]