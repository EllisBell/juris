from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from jurisapp.forms import UserLoginForm


urlpatterns = [
    path('', views.index, name='juris_index'),
    re_path('search_relevant/$', views.search_relevant, name='search_relevant'),
    re_path('search_recent/$', views.search_recent, name='search_recent'),    
    re_path('save_search/$', views.save_search, name='save_search'),
    re_path('suggest_processo/$', views.suggest_processo, name='suggest_processo'),
    path('acordao/<int:acordao_id>/', views.acordao, name='acordao'),
    path('acordao/<int:acordao_id>/pdf/', views.acordao_pdf, name='acordao_pdf'),
    path('recentes', views.recent_acordaos, name='recent_acordaos'),
    path('guardar-acordao/', views.save_acordao, name='save-acordao'),
    # Registration and authentication urls
    path('registar/', views.register, name='register'), 
    path('email-ativacao-enviado/<str:email>/', views.account_activation_sent, name='account_activation_sent'),
    path('conta-ativada/', views.account_activated, name='account_activated'),
    path('reenviar/', views.resend_confirmation_email, name='resend_confirmation_email'),
    path('ativar/<str:uidb64>/<str:token>/', views.activate_account, name='activate_account'),
    path('entrar/', auth_views.LoginView.as_view(template_name='jurisapp/registration/login.html', authentication_form=UserLoginForm), name='juris_login'),
    path('sair/', auth_views.LogoutView.as_view(template_name='jurisapp/registration/logged_out.html'), name='juris_logout'),
    path('redefinir-passe/', 
         auth_views.PasswordResetView.as_view
        (
            template_name='jurisapp/registration/password_reset.html', 
            email_template_name='jurisapp/registration/password_reset_email.html'
        ), 
        name='password_reset'),
    path('email-passe-enviado/', auth_views.PasswordResetDoneView.as_view(template_name='jurisapp/registration/password_reset_done.html'), name='password_reset_done'),
    path('confirmar-redefinicao-passe/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='jurisapp/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('palavra-passe-alterada', auth_views.PasswordResetCompleteView.as_view(template_name='jurisapp/registration/password_reset_complete.html'), name='password_reset_complete'),
    # Dossier urls
    path('dossier/', views.dossier_home, name='dossier_home'), 
    path('dossier/<int:folder_id>', views.folder_detail, name='folder_detail'),
    # Static pages urls
    path('termos', TemplateView.as_view(template_name='jurisapp/termos.html'), name='termos'),
    path('sobre', TemplateView.as_view(template_name='jurisapp/sobre.html'), name='sobre'),
]