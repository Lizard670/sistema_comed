import datetime
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Curso, Turma, Aluno, Prontuario, Usuario

class Command(BaseCommand):
    help = "Popula o banco de dados com dados de teste reais para validação do sistema CoMed."

    def handle(self, *args, **options):
        self.stdout.write("Populando banco de dados...")

        # Superusuário
        admin_user, criado = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@comed.com",
                "is_staff": True,
                "is_superuser": True
            }
        )
        if criado:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Superusuário 'admin' com senha 'admin123' criado!"))
        else:
            self.stdout.write("Superusuário 'admin' já existe.")

        # Perfil do Profissional
        usuario_profissional, _ = Usuario.objects.get_or_create(
            matricula="FUNC001",
            user=admin_user,
            defaults={"nascimento": datetime.date(1988, 7, 24)}
        )

        # Criar Cursos
        cursos_data = ["Técnico em Informática", "Técnico em Alimentos", "Técnico em Biocombustíveis"]
        cursos = []
        for nome_curso in cursos_data:
            c, _ = Curso.objects.get_or_create(nome=nome_curso)
            cursos.append(c)

        # Criar Turmas
        turmas = []
        turmas_nomes = [
            ('TIA1'),
            ('TIB1'),
            ('TAA1'),
            ('TAB1'),
            ('TBA1'),
            ('TBB1'),
            ('TI2'),
            ('TA2'),
            ('TB2'),
            ('TI3'),
            ('TA3'),
            ('TB3'),
            ('TI4'),
            ('TA4'),
            ('TB4')
        ]
        for nome_turma in turmas_nomes:
            # Associa os de Informática aos primeiros, Alimentos aos do meio, etc.
            if nome_turma.startswith("TI"):
                curso = cursos[0]
            elif nome_turma.startswith("TA"):
                curso = cursos[1]
            else:
                curso = cursos[2]
            
            t, _ = Turma.objects.get_or_create(nome=nome_turma, curso=curso, ano=nome_turma[-1:])
            turmas.append(t)

        # Criar Alunos
        alunos_data = [
            ('20261981001', 'João Victor Santos Silva',  'Maria Aparecida Silva', 'TIA1'),
            ('20261981002', 'Ana Clara Oliveira Souza',  'José Carlos Oliveira',  'TIA1'),
            ('20261981003', 'Lucas Gabriel Almeida',     'Patrícia Almeida',      'TIB1'),
            ('20261981004', 'Mariana Costa Rodrigues',   'Fernanda Costa',        'TIB1'),
            ('20261982005', 'Rafael Henrique Pereira',   'Carla Pereira',         'TAA1'),
            ('20261982006', 'Isabela Martins Lima',      'Roberto Martins',       'TAA1'),
            ('20261982007', 'Gabriel Fernandes Rocha',   'Ana Fernandes',         'TAB1'),
            ('20261982008', 'Beatriz Santos Oliveira',   'Paulo Santos',          'TAB1'),
            ('20261983009', 'Thiago Henrique Costa',     'Cláudia Costa',         'TBA1'),
            ('20261983010', 'Larissa Beatriz Alves',     'Marcos Alves',          'TBA1'),
            ('20261983011', 'Bruno Miguel Souza',        'Renata Souza',          'TBB1'),
            ('20261983012', 'Camila Rodrigues Pereira',  'Ricardo Pereira',       'TBB1'),
            ('20251981013', 'Pedro Lucas Fernandes',     'Sônia Fernandes',       'TI2'),
            ('20251981014', 'Julia Mendes Silva',        'André Mendes',          'TI2'),
            ('20251982015', 'Felipe Augusto Costa',      'Tatiana Costa',         'TA2'),
            ('20251982016', 'Nicole Santos Lima',        'Eduardo Santos',        'TA2'),
            ('20251983017', 'Matheus Vinicius Souza',    'Marisa Souza',          'TB2'),
            ('20251983018', 'Gabriela Ferreira Costa',   'Antônio Ferreira',      'TB2'),
            ('20241981019', 'Enzo Gabriel Oliveira',     'Sandra Oliveira',       'TI3'),
            ('20241981020', 'Valentina Santos Silva',    'Fábio Silva',           'TI3'),
            ('20241982021', 'Arthur Henrique Pereira',   'Lúcia Pereira',         'TA3'),
            ('20241982022', 'Helena Martins Rocha',      'Ricardo Martins',       'TA3'),
            ('20241983023', 'Theo Miguel Alves',         'Cristina Alves',        'TB3'),
            ('20241983024', 'Laura Beatriz Costa',       'Roberto Costa',         'TB3'),
            ('20231981025', 'Davi Lucas Santos',         'Patrícia Santos',       'TI4'),
            ('20231981026', 'Sophia Fernandes Oliveira', 'André Oliveira',        'TI4'),
            ('20231982027', 'Bernardo Henrique Silva',   'Márcia Silva',          'TA4'),
            ('20231982028', 'Manuela Rodrigues Pereira', 'Paulo Pereira',         'TA4'),
            ('20231983029', 'Noah Miguel Souza',         'Renata Souza',          'TB4'),
            ('20231983030', 'Alice Santos Lima',         'Marcos Lima',           'TB4'),
        ]

        alunos = []
        for matricula, nome, responsavel, nome_turma in alunos_data:
            turma_obj = next(t for t in turmas if t.nome == nome_turma)
            aluno_obj, _ = Aluno.objects.get_or_create(
                matricula=matricula,
                defaults={
                    "nome": nome,
                    "nascimento": datetime.date(random.randint(2006, 2010), random.randint(1, 12), random.randint(1, 28)),
                    "nome_responsavel": responsavel,
                    "turma": turma_obj,
                    "tipo_sanguineo": random.choice(["A+", "O+", "A-", "O-", "AB+"]),
                    "peso": Decimal(f"{random.uniform(50.0, 75.0):.2f}"),
                    "altura": Decimal(f"{random.uniform(1.55, 1.85):.2f}")
                }
            )
            alunos.append(aluno_obj)

        # Criar Prontuários
        descricoes_atendimento = [
            "Estudante queixou-se de dor de cabeça leve. Administrado analgésico e mantido em repouso por 30 minutos.",
            "Apresentou sintomas de náusea e dor abdominal. Recomendado retorno para casa e consulta médica externa.",
            "Escoriação leve no joelho esquerdo sofrida durante atividade física. Realizado curativo simples.",
            "Queixa de dor de garganta e febre baixa de 37.8°C. Orientado a buscar unidade de saúde pública."
        ]

        tipos_atend = ["consulta", "urgencia", "medicacao"]

        # Gera pelo menos 1 prontuário para cada aluno para podermos testar com qualquer um
        for i, aluno in enumerate(alunos):
            # Garante até 2 prontuários por aluno
            for k in range(random.randint(1, 4)):
                data_atendimento = datetime.date.today() - datetime.timedelta(days=random.randint(0, 180))
                Prontuario.objects.get_or_create(
                    aluno=aluno,
                    data=data_atendimento,
                    horario_inicio=datetime.time(random.randint(8, 11), 0),
                    horario_fim=datetime.time(random.randint(12, 17), 30),
                    defaults={
                        "descricao": random.choice(descricoes_atendimento),
                        "tipo_atendimento": random.choice(tipos_atend),
                        "status": "finalizado",
                        "usuario": usuario_profissional
                    }
                )

        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso."))
