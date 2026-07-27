from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UsuarioViewSet,
    UsuarioDetailView,
    CursoViewSet,
    CursoDetailView,
    TurmaViewSet,
    TurmaDetailView,
    AlunoViewSet,
    AlunoView,
    AlunoProntuariosView,
    ProntuarioViewSet,
    ProntuarioDetailView,
    DeclaracaoCreateView,
    DeclaracaoDetailView,
    ValidarDeclaracaoView,
)

router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='api-cursos')
router.register(r'turmas', TurmaViewSet, basename='api-turmas')
router.register(r'alunos', AlunoViewSet, basename='api-alunos')
router.register(r'prontuarios', ProntuarioViewSet, basename='api-prontuarios')

urlpatterns = [
    path('', include(router.urls)),

    path('usuario/<int:pk>/', UsuarioDetailView.as_view(), name='api-usuario'),
    path('curso/<int:pk>/', CursoDetailView.as_view(), name='api-curso'),
    path('turma/<int:pk>/', TurmaDetailView.as_view(), name='api-turma'),
    path('aluno/<int:pk>/', AlunoView.as_view(), name='api-aluno'),
    path('aluno/<int:pk>/prontuarios/', AlunoProntuariosView.as_view(), name='api-aluno-prontuarios'),
    path('prontuario/<int:pk>/', ProntuarioDetailView.as_view(), name='api-prontuario'),
    path('declaracao/', DeclaracaoCreateView.as_view(), name='api-declaracao-criar'),
    path('declaracao/<int:pk>/', DeclaracaoDetailView.as_view(), name='api-declaracao'),
    path('validar/<str:codigo>/', ValidarDeclaracaoView.as_view(), name='api-validar-declaracao'),
]