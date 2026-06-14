from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
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
    UsuarioListSerializer,
    UsuarioDetailSerializer,
    CursoListSerializer,
    CursoDetailSerializer,
    TurmaListSerializer,
    TurmaDetailSerializer,
    AlunoListSerializer,
    AlunoDetailSerializer,
    ProntuarioListSerializer,
    ProntuarioDetailSerializer,
    DeclaracaoSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return UsuarioListSerializer

        return UsuarioDetailSerializer


class UsuarioDetailView(RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioDetailSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CursoListSerializer

        return CursoDetailSerializer
    

class CursoDetailView(RetrieveAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoDetailSerializer


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TurmaListSerializer

        return TurmaDetailSerializer


class TurmaDetailView(RetrieveAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaDetailSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AlunoListSerializer

        return AlunoDetailSerializer
    

class AlunoDetailView(RetrieveAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoDetailSerializer

    # Rota: api/aluno/{id}/prontuarios/
    @action(detail=True, methods=["get"], url_path="prontuarios")
    def prontuarios(self, request, pk=None):
        aluno = self.get_object()

        prontuarios = Prontuario.objects.filter(aluno=aluno)
        serializer = ProntuarioListSerializer(prontuarios, many=True)

        return Response(serializer.data)


class ProntuarioViewSet(viewsets.ModelViewSet):
    queryset = Prontuario.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProntuarioListSerializer

        return ProntuarioDetailSerializer


class ProntuarioDetailView(RetrieveAPIView):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioDetailSerializer


class DeclaracaoViewSet(viewsets.ModelViewSet):
    queryset = Declaracao.objects.all()
    serializer_class = DeclaracaoSerializer


class DeclaracaoDetailView(RetrieveAPIView):
    queryset = Declaracao.objects.all()
    serializer_class = DeclaracaoSerializer