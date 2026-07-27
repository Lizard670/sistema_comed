from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic.base import TemplateView

urlpatterterns = [
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="templates/logar.html"), name = "login"),
    path("", TemplateView.as_view(template_name = "templates/index.html"), name="index"),
    #path("logar", views.pagina_logar, name="logar"),
    #path("registrar", views.pagina_registrar, name="registrar"),
    path("resetar_senha", views.pagina_resetar_senha, name="resetar_senha"),
    path("estudantes", views.pagina_estudantes, name="estudantes"),
    path("prontuario", views.pagina_prontuario, name="prontuario"),
]