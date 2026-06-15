from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, ListAPIView
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
    serializer_class = UsuarioDetailSerializer

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

    @action(detail=True, methods=["get"])
    def prontuarios(self, request, pk=None):
        aluno = self.get_object()

        prontuarios = Prontuario.objects.filter(aluno=aluno)
        serializer = ProntuarioDetailSerializer(prontuarios, many=True)

        return Response(serializer.data)


class AlunoView(RetrieveAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoDetailSerializer

class ProntuarioViewSet(viewsets.ModelViewSet):
    queryset = Prontuario.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProntuarioListSerializer

        return ProntuarioDetailSerializer


class ProntuarioDetailView(RetrieveAPIView):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioDetailSerializer


class AlunoProntuariosView(ListAPIView):
    serializer_class = ProntuarioListSerializer

    def get_queryset(self):
        return Prontuario.objects.filter(
            aluno_id=self.kwargs["pk"]
        )


class DeclaracaoViewSet(viewsets.ModelViewSet):
    queryset = Declaracao.objects.all()
    serializer_class = DeclaracaoSerializer


class DeclaracaoDetailView(RetrieveAPIView):
    queryset = Declaracao.objects.all()
    serializer_class = DeclaracaoSerializer