from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UsuarioViewSet,
    CursoViewSet,
    TurmaViewSet,
    AlunoViewSet,
    ProntuarioViewSet,
    DeclaracaoViewSet,
    UsuarioDetailView,
    CursoDetailView,
    TurmaDetailView,
    AlunoDetailView,
    ProntuarioDetailView,
    DeclaracaoDetailView
)

router = DefaultRouter()

router.register(r'usuarios', UsuarioViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'turmas', TurmaViewSet)
router.register(r'alunos', AlunoViewSet)
router.register(r'prontuarios', ProntuarioViewSet)
router.register(r'declaracoes', DeclaracaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('usuario/<int:pk>/', UsuarioDetailView.as_view(), name='usuario'),
    path('curso/<int:pk>/', CursoDetailView.as_view(), name='curso'),
    path('turma/<int:pk>/', TurmaDetailView.as_view(), name='turma'),
    path('aluno/<int:pk>/', AlunoDetailView.as_view(), name='aluno'),
    path('prontuario/<int:pk>/', ProntuarioDetailView.as_view(), name='prontuario'),
    path('declaracao/<int:pk>/', DeclaracaoDetailView.as_view(), name='declaracao')
]