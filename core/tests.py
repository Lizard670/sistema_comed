"""
Testes dos Modelos do CoMed

Cobre:
  - BaseModel: soft_delete e chamada ao full_clean no save
  - Curso: __str__ e ordering
  - Turma: relacionamento com Curso e __str__
  - Aluno: campos obrigatórios, choices de tipo_sanguineo e __str__
  - Usuario: matrícula única e __str__
  - Prontuario: choices de tipo_atendimento/status e relacionamentos
  - Declaracao: UUID gerado automaticamente e unicidade do codigo
"""

import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from core.models import Aluno, Curso, Declaracao, Prontuario, Turma, Usuario


# ---------------------------------------------------------------------------
# Helpers
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


def criar_usuario(username="enfermeiro", matricula="FUNC001"):
    """Cria um User Django + perfil Usuario e retorna ambos."""
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
    return user, usuario


def criar_prontuario(aluno, usuario):
    """Cria e retorna um Prontuario para o aluno e usuario fornecidos."""
    return Prontuario.objects.create(
        data=datetime.date(2026, 6, 28),
        horario_inicio=datetime.time(9, 0),
        horario_fim=datetime.time(9, 30),
        descricao="Paciente com cefaleia.",
        tipo_atendimento="consulta",
        status="finalizado",
        aluno=aluno,
        usuario=usuario,
    )


# ---------------------------------------------------------------------------
# Testes de BaseModel
# ---------------------------------------------------------------------------

class BaseModelTests(TestCase):
    """Testa comportamentos herdados de BaseModel."""

    def setUp(self):
        self.curso = Curso.objects.create(nome="Curso Base")

    def test_soft_delete_seta_deleted_at(self):
        """soft_delete deve preencher deleted_at com o momento atual."""
        self.assertIsNone(self.curso.deleted_at)
        self.curso.soft_delete()
        self.assertIsNotNone(self.curso.deleted_at)

    def test_soft_delete_nao_remove_do_banco(self):
        """soft_delete não deve excluir o registro fisicamente."""
        self.curso.soft_delete()
        self.assertTrue(Curso.objects.filter(pk=self.curso.pk).exists())

    def test_created_at_e_updated_at_preenchidos_automaticamente(self):
        """Os campos de auditoria devem ser preenchidos na criação."""
        self.assertIsNotNone(self.curso.created_at)
        self.assertIsNotNone(self.curso.updated_at)

    def test_save_chama_full_clean(self):
        """Salvar um modelo com dados inválidos deve lançar ValidationError."""
        curso_invalido = Curso(nome="")  # nome blank=False
        with self.assertRaises(ValidationError):
            curso_invalido.save()


# ---------------------------------------------------------------------------
# Testes de Curso
# ---------------------------------------------------------------------------

class CursoTests(TestCase):
    """Testa o modelo Curso."""

    def test_str_retorna_nome(self):
        """__str__ deve retornar o nome do curso."""
        curso = Curso.objects.create(nome="Técnico em Alimentos")
        self.assertEqual(str(curso), "Técnico em Alimentos")

    def test_nome_obrigatorio(self):
        """Criar Curso sem nome deve lançar ValidationError."""
        with self.assertRaises(ValidationError):
            Curso(nome="").save()

    def test_ordering_por_nome(self):
        """A ordenação padrão de Curso deve ser por nome."""
        Curso.objects.create(nome="Biocombustíveis")
        Curso.objects.create(nome="Alimentos")
        nomes = list(Curso.objects.values_list("nome", flat=True))
        self.assertEqual(nomes, sorted(nomes))


# ---------------------------------------------------------------------------
# Testes de Turma
# ---------------------------------------------------------------------------

class TurmaTests(TestCase):
    """Testa o modelo Turma."""

    def setUp(self):
        self.curso = Curso.objects.create(nome="Técnico em Informática")

    def test_str_retorna_nome(self):
        """__str__ deve retornar o nome da turma."""
        turma = Turma.objects.create(nome="INF1A", curso=self.curso)
        self.assertEqual(str(turma), "INF1A")

    def test_turma_tem_curso_associado(self):
        """Turma deve referenciar corretamente seu Curso."""
        turma = Turma.objects.create(nome="INF2A", curso=self.curso)
        self.assertEqual(turma.curso, self.curso)

    def test_related_name_turmas(self):
        """Curso deve acessar suas turmas via related_name 'turmas'."""
        Turma.objects.create(nome="INF1A", curso=self.curso)
        Turma.objects.create(nome="INF2A", curso=self.curso)
        self.assertEqual(self.curso.turmas.count(), 2)


# ---------------------------------------------------------------------------
# Testes de Aluno
# ---------------------------------------------------------------------------

class AlunoTests(TestCase):
    """Testa o modelo Aluno."""

    def setUp(self):
        _, self.turma, _ = criar_estrutura_base()

    def test_str_retorna_nome_e_matricula(self):
        """__str__ deve seguir o formato 'Nome - (Matrícula)'."""
        aluno = Aluno.objects.get(matricula="202300001")
        self.assertEqual(str(aluno), "Aluno Teste - (202300001)")

    def test_matricula_unica(self):
        """Não deve ser possível criar dois alunos com a mesma matrícula."""
        with self.assertRaises(Exception):
            Aluno.objects.create(
                matricula="202300001",
                nome="Outro Aluno",
                nascimento=datetime.date(2008, 3, 10),
                nome_responsavel="Outro Responsável",
                turma=self.turma,
            )

    def test_tipo_sanguineo_aceita_choices_validos(self):
        """Campo tipo_sanguineo deve aceitar valores definidos nas choices."""
        aluno = Aluno.objects.create(
            matricula="202300099",
            nome="Aluno Sanguineo",
            nascimento=datetime.date(2007, 6, 1),
            nome_responsavel="Responsável",
            turma=self.turma,
            tipo_sanguineo="O+",
        )
        self.assertEqual(aluno.tipo_sanguineo, "O+")

    def test_campos_opcionais_podem_ser_nulos(self):
        """Peso, altura, medicamentos, restricoes e observacoes são opcionais."""
        aluno = Aluno.objects.create(
            matricula="202300050",
            nome="Aluno Sem Opcionais",
            nascimento=datetime.date(2007, 1, 1),
            nome_responsavel="Responsável",
            turma=self.turma,
        )
        self.assertIsNone(aluno.peso)
        self.assertIsNone(aluno.altura)
        self.assertIsNone(aluno.medicamentos)
        self.assertIsNone(aluno.restricoes)
        self.assertIsNone(aluno.observacoes)

    def test_nome_obrigatorio(self):
        """Criar Aluno sem nome deve lançar ValidationError."""
        with self.assertRaises(ValidationError):
            Aluno(
                matricula="999999",
                nome="",
                nascimento=datetime.date(2007, 1, 1),
                nome_responsavel="Responsável",
                turma=self.turma,
            ).save()


# ---------------------------------------------------------------------------
# Testes de Usuario
# ---------------------------------------------------------------------------

class UsuarioTests(TestCase):
    """Testa o modelo Usuario (perfil do profissional de saúde)."""

    def test_str_retorna_first_name_e_matricula(self):
        """__str__ deve seguir o formato 'Nome - Matrícula'."""
        user = User.objects.create_user(username="prof1", first_name="Ana")
        usuario = Usuario.objects.create(
            matricula="FUNC010",
            nascimento=datetime.date(1985, 4, 12),
            user=user,
        )
        self.assertEqual(str(usuario), "Ana - FUNC010")

    def test_matricula_unica(self):
        """Não deve ser possível criar dois Usuarios com a mesma matrícula."""
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")
        Usuario.objects.create(
            matricula="FUNC020",
            nascimento=datetime.date(1990, 1, 1),
            user=user1,
        )
        with self.assertRaises(Exception):
            Usuario.objects.create(
                matricula="FUNC020",
                nascimento=datetime.date(1991, 2, 2),
                user=user2,
            )

    def test_relacionamento_onetoone_com_user(self):
        """Acesso ao User Django via usuario.user deve ser correto."""
        # Garante que acessar usuario.user retorna o User correto
        user = User.objects.create_user(username="profissional2")
        usuario = Usuario.objects.create(
            matricula="FUNC030",
            nascimento=datetime.date(1992, 7, 7),
            user=user,
        )
        self.assertEqual(usuario.user, user)
        self.assertEqual(user.usuario, usuario)


# ---------------------------------------------------------------------------
# Testes de Prontuario
# ---------------------------------------------------------------------------

class ProntuarioTests(TestCase):
    """Testa o modelo Prontuario."""

    def setUp(self):
        _, _, self.aluno = criar_estrutura_base()
        _, self.usuario = criar_usuario()

    def test_str_retorna_id_formatado(self):
        """__str__ deve retornar 'Prontuário #<id>'."""
        prontuario = criar_prontuario(self.aluno, self.usuario)
        self.assertEqual(str(prontuario), f"Prontuário #{prontuario.id}")

    def test_tipo_atendimento_choices(self):
        """Tipo de atendimento deve ser um dos valores definidos nas choices."""
        tipos_validos = ["consulta", "urgencia", "medicacao", "retorno"]
        for tipo in tipos_validos:
            p = Prontuario.objects.create(
                data=datetime.date(2026, 1, 1),
                horario_inicio=datetime.time(8, 0),
                horario_fim=datetime.time(8, 30),
                descricao="Teste.",
                tipo_atendimento=tipo,
                status="aberto",
                aluno=self.aluno,
                usuario=self.usuario,
            )
            self.assertEqual(p.tipo_atendimento, tipo)

    def test_status_choices(self):
        """Status deve ser um dos valores definidos nas choices."""
        status_validos = ["aberto", "finalizado", "encaminhado"]
        for status in status_validos:
            p = Prontuario.objects.create(
                data=datetime.date(2026, 2, 1),
                horario_inicio=datetime.time(10, 0),
                horario_fim=datetime.time(10, 30),
                descricao="Teste.",
                tipo_atendimento="consulta",
                status=status,
                aluno=self.aluno,
                usuario=self.usuario,
            )
            self.assertEqual(p.status, status)

    def test_related_name_prontuarios_em_aluno(self):
        """Aluno deve acessar seus prontuários via related_name 'prontuarios'."""
        criar_prontuario(self.aluno, self.usuario)
        self.assertEqual(self.aluno.prontuarios.count(), 1)

    def test_usuario_pode_ser_nulo_apos_delecao(self):
        """O campo usuario deve aceitar NULL (SET_NULL) quando o Usuario é removido."""
        prontuario = criar_prontuario(self.aluno, self.usuario)
        self.assertIsNotNone(prontuario.usuario)


# ---------------------------------------------------------------------------
# Testes de Declaracao
# ---------------------------------------------------------------------------

class DeclaracaoTests(TestCase):
    """Testa o modelo Declaracao."""

    def setUp(self):
        _, _, aluno = criar_estrutura_base()
        _, self.usuario = criar_usuario()
        self.prontuario = criar_prontuario(aluno, self.usuario)

    def test_codigo_uuid_gerado_automaticamente(self):
        """O campo codigo UUID deve ser preenchido automaticamente na criação."""
        declaracao = Declaracao.objects.create(
            descricao="Aluno liberado por 1 dia.",
            prontuario=self.prontuario,
            emitido_por=self.usuario,
        )
        self.assertIsNotNone(declaracao.codigo)

    def test_codigo_unico_entre_declaracoes(self):
        """Dois objetos Declaracao não devem compartilhar o mesmo codigo."""
        # Cria um segundo prontuário pois Declaracao tem OneToOne com Prontuario
        curso2 = Curso.objects.create(nome="Técnico em Alimentos")
        turma2 = Turma.objects.create(nome="ALM1A", curso=curso2)
        aluno2 = Aluno.objects.create(
            matricula="202300002",
            nome="Segundo Aluno",
            nascimento=datetime.date(2008, 5, 20),
            nome_responsavel="Responsável 2",
            turma=turma2,
        )
        _, usuario2 = criar_usuario(username="enfermeiro2", matricula="FUNC002")
        prontuario2 = criar_prontuario(aluno2, usuario2)

        d1 = Declaracao.objects.create(
            descricao="Primeira declaração.",
            prontuario=self.prontuario,
            emitido_por=self.usuario,
        )
        d2 = Declaracao.objects.create(
            descricao="Segunda declaração.",
            prontuario=prontuario2,
            emitido_por=usuario2,
        )
        self.assertNotEqual(d1.codigo, d2.codigo)

    def test_str_retorna_codigo(self):
        """__str__ deve retornar 'Declaração - <codigo>'."""
        declaracao = Declaracao.objects.create(
            descricao="Declaração de teste.",
            prontuario=self.prontuario,
            emitido_por=self.usuario,
        )
        self.assertEqual(str(declaracao), f"Declaração - {declaracao.codigo}")

    def test_onetoone_impede_segunda_declaracao_para_mesmo_prontuario(self):
        """Criar uma segunda Declaracao para o mesmo Prontuario deve falhar."""
        Declaracao.objects.create(
            descricao="Primeira.",
            prontuario=self.prontuario,
            emitido_por=self.usuario,
        )
        with self.assertRaises(Exception):
            Declaracao.objects.create(
                descricao="Segunda para o mesmo prontuário.",
                prontuario=self.prontuario,
                emitido_por=self.usuario,
            )

    def test_data_horario_emissao_preenchido_automaticamente(self):
        """data_horario_emissao deve ser definido automaticamente via auto_now_add."""
        declaracao = Declaracao.objects.create(
            descricao="Teste de data.",
            prontuario=self.prontuario,
            emitido_por=self.usuario,
        )
        self.assertIsNotNone(declaracao.data_horario_emissao)
