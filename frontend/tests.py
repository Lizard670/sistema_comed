"""
Testes do Frontend do CoMed

Cobre:
  - Redirecionamento de rotas protegidas para usuário não autenticado
  - Fluxo de login/logout via auth_views.LoginView
  - pagina_inicial: acesso autenticado retorna 200
  - pagina_prontuario: GET vazio, GET com pk, POST criar, POST editar, POST declaração
  - pagina_validar_declaracao: rota pública, contexto passado ao template
  - Formulários Prontuario e Estudante: campos obrigatórios e choices corretos
"""

import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from core.models import Aluno, Curso, Declaracao, Prontuario, Turma, Usuario


# ---------------------------------------------------------------------------
# Helpers (mesmo padrão dos helpers em api/tests.py)
# ---------------------------------------------------------------------------

def criar_estrutura_base():
    """Cria Curso → Turma → Aluno e retorna os três objetos."""
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


def criar_usuario_e_prontuario(aluno, username="enfermeiro", matricula="FUNC001"):
    """Cria um User + Usuario + Prontuario de teste."""
    user = User.objects.create_user(
        username=username,
        password="senha123",
        first_name="Enfermeiro",
    )
    usuario = Usuario.objects.create(
        matricula=matricula,
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


# ---------------------------------------------------------------------------
# Testes de Autenticação e Redirecionamentos
# ---------------------------------------------------------------------------

class AutenticacaoTests(TestCase):
    """Testa que rotas protegidas redirecionam usuários não autenticados."""

    def setUp(self):
        self.client = Client()
        _, _, self.aluno = criar_estrutura_base()
        self.user, _, _ = criar_usuario_e_prontuario(self.aluno)

    def test_pagina_inicial_redireciona_sem_login(self):
        """GET '/' sem autenticação deve redirecionar para /logar/."""
        resp = self.client.get(reverse("index"))
        self.assertRedirects(resp, "/logar/?next=/", fetch_redirect_response=False)

    def test_pagina_inicial_acessivel_com_login(self):
        """GET '/' autenticado deve retornar 200."""
        self.client.force_login(self.user)
        resp = self.client.get(reverse("index"))
        self.assertEqual(resp.status_code, 200)

    def test_pagina_estudantes_redireciona_sem_login(self):
        """GET '/estudantes' sem autenticação deve redirecionar para /logar/."""
        resp = self.client.get(reverse("estudantes"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/logar/", resp["Location"])

    def test_pagina_prontuario_redireciona_sem_login(self):
        """GET '/prontuario/' sem autenticação deve redirecionar para /logar/."""
        resp = self.client.get(reverse("prontuario"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/logar/", resp["Location"])

    def test_pagina_validar_declaracao_e_publica(self):
        """GET '/validar/' deve ser acessível sem autenticação."""
        resp = self.client.get(reverse("validar_declaracao"))
        self.assertEqual(resp.status_code, 200)


# ---------------------------------------------------------------------------
# Testes de Login e Logout
# ---------------------------------------------------------------------------

class LoginLogoutTests(TestCase):
    """Testa o fluxo de login e logout."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="teste_login",
            password="senha_segura_123",
        )

    def test_get_pagina_login_retorna_200(self):
        """GET '/logar/' deve retornar 200 com o formulário."""
        resp = self.client.get(reverse("login"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "logar.html")

    def test_login_com_credenciais_corretas_redireciona(self):
        """POST com credenciais válidas deve autenticar e redirecionar."""
        resp = self.client.post(reverse("login"), {
            "username": "teste_login",
            "password": "senha_segura_123",
        })
        # Django auth redireciona para LOGIN_REDIRECT_URL = '/'
        self.assertRedirects(resp, "/", fetch_redirect_response=False)

    def test_login_com_credenciais_erradas_retorna_formulario(self):
        """POST com credenciais inválidas deve retornar 200 com erros."""
        resp = self.client.post(reverse("login"), {
            "username": "teste_login",
            "password": "senha_errada",
        })
        self.assertEqual(resp.status_code, 200)

    def test_logout_encerra_sessao_e_redireciona(self):
        """GET '/deslogar/' deve encerrar a sessão e redirecionar para /logar/."""
        self.client.force_login(self.user)
        resp = self.client.get(reverse("logout"))
        self.assertRedirects(resp, reverse("login"), fetch_redirect_response=False)
        # Após deslogar, a página inicial deve redirecionar de volta para login
        resp2 = self.client.get(reverse("index"))
        self.assertEqual(resp2.status_code, 302)


# ---------------------------------------------------------------------------
# Testes de pagina_prontuario
# ---------------------------------------------------------------------------

class PaginaProntuarioTests(TestCase):
    """Testa a view pagina_prontuario (GET e POST)."""

    def setUp(self):
        self.client = Client()
        _, _, self.aluno = criar_estrutura_base()
        self.user, self.usuario, self.prontuario = criar_usuario_e_prontuario(self.aluno)
        self.client.force_login(self.user)

    def test_get_prontuario_vazio_retorna_200(self):
        """GET '/prontuario/' sem pk deve retornar 200 com formulário vazio."""
        resp = self.client.get(reverse("prontuario"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "prontuario.html")

    def test_get_prontuario_com_pk_existente_retorna_200(self):
        """GET '/prontuario/<pk>/' com pk válido deve retornar 200 com dados preenchidos."""
        resp = self.client.get(
            reverse("prontuario", kwargs={"pk": self.prontuario.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "prontuario.html")

    def test_get_prontuario_com_pk_inexistente_retorna_400(self):
        """GET '/prontuario/<pk>/' com pk inválido deve retornar 400."""
        resp = self.client.get(
            reverse("prontuario", kwargs={"pk": 99999})
        )
        self.assertEqual(resp.status_code, 400)

    def test_post_salvar_prontuario_novo_redireciona(self):
        """POST salvar_prontuario com dados válidos deve criar e redirecionar."""
        payload = {
            "salvar_prontuario": "1",
            "paciente": self.aluno.pk,
            "data": "2026-07-01",
            "inicio": "08:00",
            "fim": "08:30",
            "status": "aberto",
            "tipo_atendimento": "consulta",
            "descricao": "Nova queixa de dor de cabeça.",
        }
        resp = self.client.post(reverse("prontuario"), payload)
        # Deve redirecionar para o prontuário recém-criado
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/prontuario/", resp["Location"])

    def test_post_salvar_prontuario_existente_atualiza(self):
        """POST salvar_prontuario com pk existente deve atualizar o registro."""
        payload = {
            "salvar_prontuario": "1",
            "paciente": self.aluno.pk,
            "data": "2026-07-10",
            "inicio": "10:00",
            "fim": "10:45",
            "status": "finalizado",
            "tipo_atendimento": "retorno",
            "descricao": "Retorno — melhora significativa.",
        }
        resp = self.client.post(
            reverse("prontuario", kwargs={"pk": self.prontuario.pk}),
            payload,
        )
        self.assertEqual(resp.status_code, 302)
        self.prontuario.refresh_from_db()
        self.assertEqual(self.prontuario.tipo_atendimento, "retorno")
        self.assertEqual(self.prontuario.status, "finalizado")

    def test_post_salvar_declaracao_nova_cria_registro(self):
        """POST salvar_declaracao com prontuario existente deve criar Declaracao."""
        payload = {
            "salvar_declaracao": "1",
            "paciente": self.aluno.pk,
            "data": "2026-06-28",
            "inicio": "09:00",
            "fim": "09:30",
            "status": "finalizado",
            "tipo_atendimento": "consulta",
            "descricao": "Paciente com cefaleia.",
            "declaracao": "Declaro que o aluno foi atendido.",
        }
        resp = self.client.post(
            reverse("prontuario", kwargs={"pk": self.prontuario.pk}),
            payload,
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Declaracao.objects.filter(prontuario=self.prontuario).exists())

    def test_post_salvar_declaracao_existente_atualiza(self):
        """POST salvar_declaracao quando já existe deve atualizar a declaração."""
        Declaracao.objects.create(
            descricao="Texto original.",
            prontuario=self.prontuario,
            emitido_por=self.usuario,
        )
        payload = {
            "salvar_declaracao": "1",
            "paciente": self.aluno.pk,
            "data": "2026-06-28",
            "inicio": "09:00",
            "fim": "09:30",
            "status": "finalizado",
            "tipo_atendimento": "consulta",
            "descricao": "Paciente com cefaleia.",
            "declaracao": "Texto atualizado.",
        }
        self.client.post(
            reverse("prontuario", kwargs={"pk": self.prontuario.pk}),
            payload,
        )
        declaracao = Declaracao.objects.get(prontuario=self.prontuario)
        self.assertEqual(declaracao.descricao, "Texto atualizado.")

    def test_post_salvar_prontuario_sem_perfil_usuario_redireciona_com_erro(self):
        """POST sem perfil Usuario vinculado ao user deve redirecionar com err=403."""
        # Cria um User sem o perfil Usuario correspondente
        user_sem_perfil = User.objects.create_user(
            username="sem_perfil", password="senha123"
        )
        self.client.force_login(user_sem_perfil)
        payload = {
            "salvar_prontuario": "1",
            "paciente": self.aluno.pk,
            "data": "2026-07-15",
            "inicio": "11:00",
            "fim": "11:30",
            "status": "aberto",
            "tipo_atendimento": "urgencia",
            "descricao": "Urgência sem perfil.",
        }
        resp = self.client.post(reverse("prontuario"), payload)
        # Deve redirecionar (com o erro 403 embutido na URL)
        self.assertEqual(resp.status_code, 302)


# ---------------------------------------------------------------------------
# Testes de pagina_validar_declaracao
# ---------------------------------------------------------------------------

class PaginaValidarDeclaracaoTests(TestCase):
    """Testa a view pública pagina_validar_declaracao."""

    def setUp(self):
        self.client = Client()

    def test_get_sem_codigo_retorna_200(self):
        """GET '/validar/' sem código deve retornar 200."""
        resp = self.client.get(reverse("validar_declaracao"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "validar_declaracao.html")

    def test_get_com_codigo_passa_para_template(self):
        """GET '/validar/<codigo>/' deve passar o código ao contexto do template."""
        codigo_teste = "c9bf9e57-1685-4c89-bafb-ff5af830be8a"
        resp = self.client.get(
            reverse("validar_declaracao_codigo", kwargs={"codigo": codigo_teste})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["codigo"], codigo_teste)

    def test_rota_acessivel_sem_autenticacao(self):
        """A página de validação deve ser pública — sem sessão autenticada."""
        # Cliente sem nenhum login
        cliente_anonimo = Client()
        resp = cliente_anonimo.get(reverse("validar_declaracao"))
        self.assertEqual(resp.status_code, 200)


# ---------------------------------------------------------------------------
# Testes de Formulários
# ---------------------------------------------------------------------------

class FormularioProntuarioTests(TestCase):
    """Testa o formulário frontend.forms.Prontuario."""

    def setUp(self):
        _, self.turma, self.aluno = criar_estrutura_base()

    def test_formulario_valido_com_dados_corretos(self):
        """Formulário Prontuario deve ser válido com todos os campos obrigatórios."""
        from frontend.forms import Prontuario as FormProntuario
        data = {
            "paciente": self.aluno.pk,
            "data": "2026-07-01",
            "inicio": "08:00",
            "fim": "08:30",
            "status": "aberto",
            "tipo_atendimento": "consulta",
            "descricao": "Descrição de teste.",
        }
        form = FormProntuario(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_formulario_invalido_sem_paciente(self):
        """Formulário Prontuario sem paciente deve ser inválido."""
        from frontend.forms import Prontuario as FormProntuario
        data = {
            "data": "2026-07-01",
            "inicio": "08:00",
            "fim": "08:30",
            "status": "aberto",
            "tipo_atendimento": "consulta",
            "descricao": "Sem paciente.",
        }
        form = FormProntuario(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("paciente", form.errors)

    def test_formulario_invalido_sem_descricao(self):
        """Formulário Prontuario sem descrição deve ser inválido."""
        from frontend.forms import Prontuario as FormProntuario
        data = {
            "paciente": self.aluno.pk,
            "data": "2026-07-01",
            "inicio": "08:00",
            "fim": "08:30",
            "status": "aberto",
            "tipo_atendimento": "consulta",
            "descricao": "",
        }
        form = FormProntuario(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("descricao", form.errors)

    def test_choices_status_correspondem_ao_modelo(self):
        """As choices de status no formulário devem corresponder às do modelo."""
        from frontend.forms import Prontuario as FormProntuario
        from core.models import Prontuario as ModelProntuario

        form = FormProntuario()
        choices_form = set(v for v, _ in form.fields["status"].choices)
        choices_modelo = set(v for v, _ in ModelProntuario._meta.get_field("status").choices)
        self.assertEqual(choices_form, choices_modelo)

    def test_choices_tipo_atendimento_correspondem_ao_modelo(self):
        """As choices de tipo_atendimento no formulário devem corresponder às do modelo."""
        from frontend.forms import Prontuario as FormProntuario
        from core.models import Prontuario as ModelProntuario

        form = FormProntuario()
        choices_form = set(v for v, _ in form.fields["tipo_atendimento"].choices)
        choices_modelo = set(v for v, _ in ModelProntuario._meta.get_field("tipo_atendimento").choices)
        self.assertEqual(choices_form, choices_modelo)


class FormularioEstudanteTests(TestCase):
    """Testa o formulário frontend.forms.Estudante."""

    def setUp(self):
        _, self.turma, self.aluno = criar_estrutura_base()

    def test_formulario_choices_tipo_sanguineo_corretos(self):
        """As choices de tipo sanguíneo devem corresponder às do modelo Aluno."""
        from frontend.forms import Estudante as FormEstudante

        form = FormEstudante()
        choices_form = set(v for v, _ in form.fields["tipo"].choices if v)
        choices_modelo = set(v for v, _ in Aluno.TIPOS_SANGUINEOS)
        self.assertEqual(choices_form, choices_modelo)

    def test_formulario_choices_turma_carregadas(self):
        """O campo turma deve incluir todas as turmas existentes no banco."""
        from frontend.forms import Estudante as FormEstudante

        form = FormEstudante()
        # Converte ambos para str para evitar divergência de tipo (int vs str)
        pks_form = set(str(v) for v, _ in form.fields["turma"].choices if v)
        pks_banco = set(str(t.pk) for t in Turma.objects.all())
        self.assertEqual(pks_form, pks_banco)

    def test_matricula_e_obrigatoria(self):
        """Formulário Estudante sem matrícula deve ser inválido."""
        from frontend.forms import Estudante as FormEstudante

        data = {
            "nome": self.aluno.pk,
            # 'matricula' ausente intencionalmente
        }
        form = FormEstudante(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("matricula", form.errors)
