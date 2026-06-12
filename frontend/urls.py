from django.urls import path
from . import views

urlpatterns = [
    path("", views.pagina_inicial, name="index"),
    path("logar", views.pagina_logar, name="logar"),
    path("registrar", views.pagina_registrar, name="registrar"),
    path("resetar_senha", views.pagina_resetar_senha, name="resetar_senha"),
    path("estudantes", views.pagina_estudantes, name="estudantes"),
]