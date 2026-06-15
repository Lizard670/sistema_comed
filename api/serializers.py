from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers
from core.models import Usuario, Curso, Turma, Aluno, Prontuario, Declaracao

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ["first_name"]
        
class UsuarioDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Usuario
        fields =  ["id", "matricula", "user"]
    
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
        fields =  ["id", "nome"]

class CursoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields =  "__all__"

class TurmaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields =  ["id", "nome", "curso"]

class TurmaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields =  "__all__"

class AlunoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ["id", "matricula", "nome", "nome_responsavel", "turma"]

class AlunoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields =  "__all__"

class ProntuarioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prontuario
        fields = ["id", "aluno", "usuario", "data", "status"]

class ProntuarioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prontuario
        fields =  "__all__"

class DeclaracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaracao
        fields = "__all__"
