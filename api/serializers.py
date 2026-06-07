from django.urls import path, include
from django.contrib.auth.models import Group, User
from rest_framework import routers, serializers, viewsets
from core.models import Usuario, Curso, Turma, Aluno, Prontuario, Atestado


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "matricula", "nome"]


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ["id", "nome"]


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ["id", "nome", "curso"]

#Só em caso de não precisar de todas a informações de uma vez tirando isso tudo certo
class AlunoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ["id", "matricula", "nome", "turma"]


class AlunoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ["id", "matricula", "nome", "nascimento", "responsavel", "peso", "altura", "medicamentos_continuos", "restricoes_medicas", "tipo_sanguineo", "turma"]


class ProntuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prontuario
        fields = ["id", "data_horario", "descricao", "observacoes", "encaminhamento", "tipo_atendimento", "status","aluno", "usuario"]


class AtestadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atestado
        fields = "__all__"