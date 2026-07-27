from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path("logar/", auth_views.LoginView.as_view(template_name="logar.html"), name = "login"),
    path("deslogar/", views.pagina_deslogar, name="logout"),
    path("", views.pagina_inicial, name="index"),
    path("estudantes", views.pagina_estudantes, name="estudantes"),
    path("prontuario", views.pagina_prontuario, name="prontuario"),
]