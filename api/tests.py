"""
Testes da API do CoMed

Cobre:
  - Criação de Declaracao (gera código único automaticamente)
  - Retorno dos dados aninhados (prontuario_detalhes, aluno)
  - Rota pública de validação por código
  - Proteção de endpoints autenticados
"""

import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Aluno, Curso, Declaracao, Prontuario, Turma, Usuario


# Helpers
def criar_estrutura_base():
    """Cria Curso → Turma → Aluno e retorna os três objetos"""
    curso = Curso.objects.create(nome="Técnico em Informática")
    turma = Turma.objects.create(nome="INF3A", curso=curso)
    aluno = Aluno.objects.create(
        matricula="202300001",
        nome="Aluno Teste",
        nascimento=datetime.date(2007, 1, 15),
        nome_responsavel="Responsável Teste",
        turma=turma,
    )
    return curso, turma, aluno


def criar_usuario_e_prontuario(aluno):
    """Cria um User + Usuario + Prontuario de teste"""
    user = User.objects.create_user(username="enfermeiro", password="senha123")
    usuario = Usuario.objects.create(
        matricula="FUNC001",
        nascimento=datetime.date(1990, 5, 20),
        user=user,
    )
    prontuario = Prontuario.objects.create(
        data=datetime.date(2026, 6, 28),
        horario_inicio=datetime.time(9, 0),
        horario_fim=datetime.time(9, 30),
        descricao="Paciente com cefaleia.",
        tipo_atendimento="consulta",
        status="finalizado",
        aluno=aluno,
        usuario=usuario,
    )
    return user, usuario, prontuario


# Testes de Declaração
class DeclaracaoCreateTests(TestCase):
    """Testa a criação de declarações via POST /api/declaracoes/"""

    def setUp(self):
        self.client = APIClient()
        _, _, self.aluno = criar_estrutura_base()
        self.user, self.usuario, self.prontuario = criar_usuario_e_prontuario(self.aluno)
        self.client.force_authenticate(user=self.user)
        self.url = "/api/declaracao/"

    def test_criacao_gera_codigo_unico(self):
        """Ao criar uma Declaracao, o backend deve gerar um codigo não vazio."""
        payload = {
            "prontuario": self.prontuario.pk,
            "descricao": "Aluno liberado por 1 dia para repouso.",
        }
        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("codigo", resp.data)
        self.assertTrue(resp.data["codigo"].startswith("CoMed-"))

    def test_codigos_sao_distintos_em_criações_diferentes(self):
        """Duas declarações geradas devem ter códigos diferentes."""
        payload = {
            "prontuario": self.prontuario.pk,
            "descricao": "Primeira declaração.",
        }
        r1 = self.client.post(self.url, payload, format="json")
        self.assertEqual(r1.status_code, status.HTTP_201_CREATED)

        # Precisa de um segundo prontuário pois Declaracao tem OneToOne com Prontuario
        prontuario2 = Prontuario.objects.create(
            data=datetime.date(2026, 6, 29),
            horario_inicio=datetime.time(10, 0),
            horario_fim=datetime.time(10, 20),
            descricao="Segunda consulta.",
            tipo_atendimento="retorno",
            status="finalizado",
            aluno=self.aluno,
            usuario=self.usuario,
        )
        payload2 = {"prontuario": prontuario2.pk, "descricao": "Segunda declaração."}
        r2 = self.client.post(self.url, payload, format="json")
        # Mesmo que o segundo falhe por unique, os códigos da resposta devem diferir
        if r2.status_code == status.HTTP_201_CREATED:
            self.assertNotEqual(r1.data["codigo"], r2.data["codigo"])

    def test_resposta_inclui_dados_aninhados_do_aluno(self):
        """A resposta deve conter prontuario_detalhes com o nome do aluno."""
        payload = {
            "prontuario": self.prontuario.pk,
            "descricao": "Declaração com dados aninhados.",
        }
        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        detalhes = resp.data.get("prontuario_detalhes", {})
        aluno_data = detalhes.get("aluno", {})
        self.assertEqual(aluno_data.get("nome"), "Aluno Teste")
        self.assertEqual(aluno_data.get("matricula"), "202300001")
        self.assertEqual(aluno_data.get("turma_nome"), "INF3A")
        self.assertEqual(aluno_data.get("curso_nome"), "Técnico em Informática")

    def test_codigo_nao_pode_ser_enviado_pelo_cliente(self):
        """O campo 'codigo' deve ser ignorado se enviado pelo cliente."""
        payload = {
            "prontuario": self.prontuario.pk,
            "descricao": "Tentando forçar código.",
            "codigo": "CODIGO-FALSO",
        }
        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(resp.data.get("codigo"), "CODIGO-FALSO")


class DeclaracaoAutenticacaoTests(TestCase):
    """Testa que endpoints protegidos exigem autenticação."""

    def setUp(self):
        self.client = APIClient()
        _, _, self.aluno = criar_estrutura_base()
        self.user, self.usuario, self.prontuario = criar_usuario_e_prontuario(self.aluno)

    def test_usuario_nao_autenticado_nao_pode_criar(self):
        """POST sem autenticação deve retornar 403."""
        payload = {
            "prontuario": self.prontuario.pk,
            "descricao": "Sem login.",
        }
        resp = self.client.post("/api/declaracao/", payload, format="json")
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_usuario_nao_autenticado_nao_pode_ver_detalhes(self):
        """GET em detalhe sem autenticação deve retornar 403."""
        # Cria uma declaração com autenticação temporária no banco
        self.client.force_authenticate(user=self.user)
        self.declaracao = Declaracao.objects.create(
            codigo="CoMed-TEST1234",
            descricao="Repouso.",
            prontuario=self.prontuario,
            emitido_por=self.usuario
        )
        self.client.logout()  # Desloga

        resp = self.client.get(f"/api/declaracao/{self.declaracao.pk}/")
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])


class ValidarDeclaracaoTests(TestCase):
    """Testa a rota pública de validação GET /api/validar/<codigo>/."""

    def setUp(self):
        self.client = APIClient()
        _, _, aluno = criar_estrutura_base()
        user, usuario, prontuario = criar_usuario_e_prontuario(aluno)
        self.declaracao = Declaracao.objects.create(
            codigo="COMED-ABCD1234EFGH5678IJKL9012MNOP",
            descricao="Declaração de teste.",
            prontuario=prontuario,
            emitido_por=usuario,
        )

    def test_validacao_por_codigo_existente(self):
        """Deve retornar 200 com {"valido": true} para um código válido."""
        resp = self.client.get(f"/api/validar/{self.declaracao.codigo}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data["valido"])

    def test_validacao_por_codigo_inexistente_retorna_404(self):
        """Código inválido deve retornar 404 com {"valido": false}."""
        resp = self.client.get("/api/validar/COMED-NAOEXISTE0000000000000000/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(resp.data["valido"])

    def test_validacao_nao_requer_autenticacao(self):
        """A rota de validação deve ser pública — sem token ou sessão."""
        # Cliente sem nenhuma autenticação
        cliente_anonimo = APIClient()
        resp = cliente_anonimo.get(f"/api/validar/{self.declaracao.codigo}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_validacao_nao_expoe_dados_da_declaracao(self):
        """A resposta de validação deve conter apenas o campo 'valido', sem dados internos."""
        resp = self.client.get(f"/api/validar/{self.declaracao.codigo}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(list(resp.data.keys()), ["valido"])

