from django.shortcuts import render
from rest_framework import viewsets

from core.models import (
    Usuario,
    Curso,
    Turma,
    Aluno,
    Prontuario,
    Atestado
)

from .serializers import (
    UsuarioSerializer,
    CursoSerializer,
    TurmaSerializer,
    AlunoListSerializer,
    AlunoDetailSerializer,
    ProntuarioSerializer,
    AtestadoSerializer
)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AlunoListSerializer

        return AlunoDetailSerializer


class ProntuarioViewSet(viewsets.ModelViewSet):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer


class AtestadoViewSet(viewsets.ModelViewSet):
    queryset = Atestado.objects.all()
    serializer_class = AtestadoSerializer