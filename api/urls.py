from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsuarioViewSet, CursoViewSet, TurmaViewSet, AlunoViewSet, ProntuarioViewSet, DeclaracaoViewSet

router = DefaultRouter()

router.register(r'usuarios', UsuarioViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'turmas', TurmaViewSet)
router.register(r'alunos', AlunoViewSet)
router.register(r'prontuarios', ProntuarioViewSet)
router.register(r'declaracoes', DeclaracaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]