import uuid

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import (
    Usuario,
    Curso,
    Turma,
    Aluno,
    Prontuario,
    Declaracao,
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
    DeclaracaoSerializer,
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
        return Prontuario.objects.filter(aluno_id=self.kwargs["pk"])


class DeclaracaoCreateView(CreateAPIView):
    queryset = Declaracao.objects.all()
    serializer_class = DeclaracaoSerializer

    def perform_create(self, serializer):
        """
        Gera automaticamente o código único do atestado (formato CoMed-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX)
        e vincula o emissor ao usuário autenticado, se disponível.

        Utiliza o UUID4 completo (32 caracteres hex / 128 bits) para minimizar o risco de colisão.
        """
        codigo = f"CoMed-{uuid.uuid4().hex.upper()}"
        emitido_por = getattr(self.request.user, 'usuario', None)
        serializer.save(codigo=codigo, emitido_por=emitido_por)


class DeclaracaoDetailView(RetrieveAPIView):
    queryset = Declaracao.objects.all()
    serializer_class = DeclaracaoSerializer


class ValidarDeclaracaoView(APIView):
    """
    Rota pública para validar a autenticidade de um atestado pelo código único.
    Não requer autenticação — qualquer pessoa pode confirmar se o atestado é legítimo.

    Retorna a validade e os dados que constam na declaração: matrícula, data e
    horários de entrada e saída do atendimento.
    Exemplo: GET /api/validar/CoMed-23A231CF5923E874AABBCCDD11223344/
    """
    permission_classes = [AllowAny]

    def get(self, request, codigo):
        declaracao = (
            Declaracao.objects.select_related("prontuario__aluno")
            .filter(codigo=codigo)
            .first()
        )
        if declaracao:
            prontuario = declaracao.prontuario
            return Response(
                {
                    "valido": True,
                    "matricula": prontuario.aluno.matricula,
                    "data_atendimento": prontuario.data.isoformat(),
                    "horario_entrada": prontuario.horario_inicio.strftime("%H:%M"),
                    "horario_saida": prontuario.horario_fim.strftime("%H:%M"),
                },
                status=status.HTTP_200_OK,
            )
        return Response({"valido": False}, status=status.HTTP_404_NOT_FOUND)
