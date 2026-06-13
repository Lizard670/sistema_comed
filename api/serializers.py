from django.urls import path, include
from django.contrib.auth.models import Group, User
from rest_framework import routers, serializers, viewsets
from rest_framework.generics import RetrieveAPIView
from core.models import Usuario, Curso, Turma, Aluno, Prontuario, Declaracao

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  "__all__"

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields =  "__all__"
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data["user"])

        try:
            usuario = Usuario.objects.create(user=user, matricula=validated_data["matricula"], nascimento=validated_data["nascimento"])
        except Exception as e:
            user.delete()
            raise e
        else:
            return usuario

class UsuarioDetailView(RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields =  "__all__"

class CursoDetailView(RetrieveAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields =  "__all__"

class TurmaDetailView(RetrieveAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

# Só em caso de não precisar de todas a informações de uma vez 
class AlunoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ["id", "matricula", "nome", "turma"]

class AlunoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields =  "__all__"

class AlunoDetailView(RetrieveAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoDetailSerializer

class ProntuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prontuario
        fields =  "__all__"

class ProntuarioDetailView(RetrieveAPIView):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer

class DeclaracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaracao
        fields = "__all__"

class AtestadoDetailView(RetrieveAPIView):
    queryset = Declaracao.objects.all()
    serializer_class = DeclaracaoSerializer
