from django.contrib.auth.models import User
from rest_framework import serializers
from core.models import Usuario, Curso, Turma, Aluno, Prontuario, Declaracao


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name"]


class UsuarioDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Usuario
        fields = ["id", "matricula", "user"]

    def create(self, validated_data):
        user = User.objects.create(**validated_data["user"])

        try:
            usuario = Usuario.objects.create(user=user)
        except Exception as e:
            user.delete()
            raise e
        else:
            return usuario


class CursoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ["id", "nome"]


class CursoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"


class TurmaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ["id", "nome", "curso"]


class TurmaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = "__all__"


class AlunoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ["id", "matricula", "nome", "nome_responsavel", "turma", "nascimento"]


class AlunoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = "__all__"


class ProntuarioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prontuario
        fields = ["id", "aluno", "usuario", "data", "tipo_atendimento", "status"]


class ProntuarioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prontuario
        fields = "__all__"


# Serializers aninhados para composição do PDF do atestado
class _AlunoAtestadoSerializer(serializers.ModelSerializer):
    """Dados do aluno necessários para compor o PDF do atestado."""
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    curso_nome = serializers.CharField(source='turma.curso.nome', read_only=True)

    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'nascimento', 'turma_nome', 'curso_nome']


class _ProntuarioAtestadoSerializer(serializers.ModelSerializer):
    """Dados do prontuário necessários para compor o PDF do atestado."""
    aluno = _AlunoAtestadoSerializer(read_only=True)

    class Meta:
        model = Prontuario
        fields = ['id', 'data', 'horario_inicio', 'horario_fim', 'tipo_atendimento', 'aluno']


class DeclaracaoSerializer(serializers.ModelSerializer):
    # Campos gerados/definidos pelo backend
    codigo = serializers.CharField(read_only=True)
    emitido_por = serializers.PrimaryKeyRelatedField(read_only=True)
    data_horario_emissao = serializers.DateTimeField(read_only=True)

    # Dados aninhados retornados na resposta para o frontend montar o PDF
    prontuario_detalhes = _ProntuarioAtestadoSerializer(source='prontuario', read_only=True)

    class Meta:
        model = Declaracao
        fields = [
            'prontuario',
            'descricao',
            'observacoes_internas',
            'codigo',
            'emitido_por',
            'data_horario_emissao',
            'prontuario_detalhes',
        ]
