"""
Management command: criar_usuario

Cria um User Django + perfil Usuario no sistema CoMed via linha de comando.
Aceita argumentos opcionais; quando omitidos, solicita os valores interativamente.

Uso:
    python manage.py criar_usuario
    python manage.py criar_usuario --username vitoriagsantos --matricula FUNC042
    python manage.py criar_usuario --superuser

Opções:
    --username      Nome de usuário para login
    --nome          Nome do profissional
    --email         E-mail do usuário
    --senha         Senha (se omitida, será solicitada de forma segura)
    --matricula     Matrícula funcional (identificador no perfil Usuario)
    --nascimento    Data de nascimento no formato AAAA-MM-DD
    --superuser     Cria o usuário como superusuário (is_staff + is_superuser) (Apenas ADM/DEVS!!!)
"""

import datetime
import getpass

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from core.models import Usuario


class Command(BaseCommand):
    help = "Cria um User Django + perfil Usuario no sistema CoMed."

    def add_arguments(self, parser):
        parser.add_argument("--username",    dest="username",    default=None)
        parser.add_argument("--nome",        dest="first_name",  default=None)
        parser.add_argument("--email",       dest="email",       default=None)
        parser.add_argument("--senha",       dest="password",    default=None)
        parser.add_argument("--matricula",   dest="matricula",   default=None)
        parser.add_argument("--nascimento",  dest="nascimento",  default=None,
                            help="Data de nascimento no formato AAAA-MM-DD")
        parser.add_argument("--superuser",   dest="superuser",
                            action="store_true", default=False,
                            help="Cria o usuário como superusuário")

    # ------------------------------------------------------------------
    # Helpers de entrada interativa
    # ------------------------------------------------------------------

    def _perguntar(self, prompt, obrigatorio=True):
        """Lê uma string do stdin; repete enquanto o campo obrigatório estiver vazio."""
        while True:
            valor = input(prompt).strip()
            if valor or not obrigatorio:
                return valor
            self.stdout.write(self.style.ERROR("  Este campo é obrigatório."))

    def _perguntar_data(self, prompt):
        """Lê e valida uma data no formato AAAA-MM-DD; repete em caso de erro."""
        while True:
            valor = input(prompt).strip()
            if not valor:
                return None
            try:
                return datetime.date.fromisoformat(valor)
            except ValueError:
                self.stdout.write(self.style.ERROR(
                    "  Formato inválido. Use AAAA-MM-DD (ex.: 1990-05-20)."
                ))

    def _perguntar_senha(self):
        """Solicita a senha duas vezes para confirmação, sem ecoar no terminal."""
        while True:
            senha = getpass.getpass("  Senha: ")
            confirmacao = getpass.getpass("  Confirme a senha: ")
            if senha == confirmacao:
                return senha
            self.stdout.write(self.style.ERROR("  As senhas não coincidem. Tente novamente."))

    # ------------------------------------------------------------------
    # Validações
    # ------------------------------------------------------------------

    def _validar_username(self, username):
        """Lança CommandError se o username já estiver em uso."""
        if User.objects.filter(username=username).exists():
            raise CommandError(f"Já existe um usuário com o username '{username}'.")

    def _validar_matricula(self, matricula):
        """Lança CommandError se a matrícula já estiver em uso."""
        if Usuario.objects.filter(matricula=matricula).exists():
            raise CommandError(f"Já existe um perfil com a matrícula '{matricula}'.")

    # ------------------------------------------------------------------
    # Handler principal
    # ------------------------------------------------------------------

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            "\n=== CoMed — Criar Usuário ==="
        ))

        # ------- Coletar dados (argumento ou prompt) -------

        username = options["username"] or self._perguntar("  Nome de usuário (login): ")
        self._validar_username(username)

        nome  = options["first_name"] or self._perguntar("  Nome completo: ", obrigatorio=False)
        email = options["email"]      or self._perguntar("  E-mail: ", obrigatorio=False)

        if options["password"]:
            password = options["password"]
        else:
            self.stdout.write("  Senha (não será exibida):")
            password = self._perguntar_senha()

        matricula = options["matricula"] or self._perguntar("  Matrícula funcional (ex.: FUNC042): ")
        self._validar_matricula(matricula)

        if options["nascimento"]:
            try:
                nascimento = datetime.date.fromisoformat(options["nascimento"])
            except ValueError:
                raise CommandError("Formato de nascimento inválido. Use AAAA-MM-DD.")
        else:
            self.stdout.write("  Data de nascimento (AAAA-MM-DD):")
            nascimento = self._perguntar_data("  > ")

        superuser = options["superuser"]

        # ------- Criar registros no banco -------

        self.stdout.write("")

        try:
            # Cria o User Django
            if superuser:
                user = User.objects.create_superuser(
                    username=username,
                    email=email or "",
                    password=password,
                    first_name=nome or "",
                )
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email or "",
                    password=password,
                    first_name=nome or "",
                )

            # Cria o perfil Usuario vinculado ao User
            usuario = Usuario.objects.create(
                matricula=matricula,
                nascimento=nascimento,
                user=user,
            )

        except Exception as e:
            # Garante que o User não fica órfão se a criação do Usuario falhar
            if 'user' in locals() and user.pk:
                user.delete()
            raise CommandError(f"Erro ao criar o usuário: {e}")

        # ------- Feedback de sucesso -------

        tipo = "Superusuário" if superuser else "Usuário"
        self.stdout.write(self.style.SUCCESS(
            f"{tipo} '{username}' criado com sucesso!"
        ))
        self.stdout.write(f"  Matrícula : {matricula}")
        self.stdout.write(f"  Nome      : {user.first_name or '(não informado)'}")
        self.stdout.write(f"  E-mail    : {user.email or '(não informado)'}")
        self.stdout.write(f"  Nascimento: {nascimento or '(não informado)'}")
        if superuser:
            self.stdout.write(self.style.WARNING(
                "  ⚠  Superusuário tem acesso total ao painel de administração."
            ))
