from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import (
    Usuario,
    Curso,
    Turma,
    Aluno,
    Prontuario,
    Declaracao
)

from .serializers import (
    UsuarioSerializer,
    CursoSerializer,
    TurmaSerializer,
    AlunoListSerializer,
    AlunoDetailSerializer,
    ProntuarioSerializer,
    DeclaracaoSerializer
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

    # Rota: api/aluno/{id}/prontuarios/
    @action(detail=True, methods=["get"], url_path="prontuarios")
    def prontuarios(self, request, pk=None):
        aluno = self.get_object()

        prontuarios = Prontuario.objects.filter(aluno=aluno)
        serializer = ProntuarioSerializer(prontuarios, many=True)

        return Response(serializer.data)
    

class ProntuarioViewSet(viewsets.ModelViewSet):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer


class DeclaracaoViewSet(viewsets.ModelViewSet):
    queryset = Declaracao.objects.all()
    serializer_class = DeclaracaoSerializer