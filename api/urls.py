from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UsuarioViewSet,
    CursoViewSet,
    TurmaViewSet,
    AlunoViewSet,
    ProntuarioViewSet,
    AtestadoViewSet
)

router = DefaultRouter()

router.register(r'usuarios', UsuarioViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'turmas', TurmaViewSet)
router.register(r'alunos', AlunoViewSet)
router.register(r'prontuarios', ProntuarioViewSet)
router.register(r'atestados', AtestadoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]