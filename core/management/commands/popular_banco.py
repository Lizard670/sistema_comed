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
        turmas_nomes = ["INF1A", "INF2A", "INF3A", "ALM1A", "ALM2A", "BIO1A"]
        for nome_turma in turmas_nomes:
            # Associa os de Informática aos primeiros, Alimentos aos do meio, etc.
            if nome_turma.startswith("INF"):
                curso = cursos[0]
            elif nome_turma.startswith("ALM"):
                curso = cursos[1]
            else:
                curso = cursos[2]
            
            t, _ = Turma.objects.get_or_create(nome=nome_turma, curso=curso)
            turmas.append(t)

        # Criar Alunos
        alunos_data = [
            ("Lucas Matheus Ferreira", "202319830001", "Maria Ferreira", "INF3A"),
            ("Maciel Souza Santos", "202319830012", "João Souza Santos", "INF3A"),
            ("Rafael Augusto Lima Costa", "202419820734", "Helena Lima Costa", "BIO1A"),
            ("Camila Beatriz Rocha Alves", "202519831456", "Cláudia Rocha Alves", "ALM1A"),
            ("Mariana Júlia Fernandes Dias", "202419821234", "Aline Fernandes Dias", "BIO1A"),
            ("Gabriel Henrique Martins Ribeiro", "202319832567", "Marcos Martins Ribeiro", "ALM2A"),
        ]

        alunos = []
        for nome, matricula, responsavel, nome_turma in alunos_data:
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
            for k in range(random.randint(1, 2)):
                data_atendimento = datetime.date.today() - datetime.timedelta(days=random.randint(0, 30))
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
