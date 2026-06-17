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
    DeclaracaoViewSet,
    UsuarioDetailView,
    CursoDetailView,
    TurmaDetailView,
    ProntuarioDetailView,
    DeclaracaoDetailView
)

router = DefaultRouter()

router.register(r'cursos', CursoViewSet)
router.register(r'turmas', TurmaViewSet)
router.register(r'alunos', AlunoViewSet)
router.register(r'prontuarios', ProntuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('usuario/<int:pk>/', UsuarioDetailView.as_view(), name='usuario'),
    path('curso/<int:pk>/', CursoDetailView.as_view(), name='curso'),
    path('turma/<int:pk>/', TurmaDetailView.as_view(), name='turma'),
    path('aluno/<int:pk>/', AlunoView.as_view(), name='aluno'),
    path("aluno/<int:pk>/prontuarios/", AlunoProntuariosView.as_view(), name="aluno-prontuarios"),
    path('prontuario/<int:pk>/', ProntuarioDetailView.as_view(), name='prontuario'),
    path('declaracao/<int:pk>/', DeclaracaoDetailView.as_view(), name='declaracao')
]