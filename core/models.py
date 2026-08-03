from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
import uuid

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
        
class Usuario(BaseModel):
    matricula = models.CharField(help_text="Matrícula do usuário", max_length=20, unique=True, db_index=True, blank=False, null=False)
    nascimento = models.DateField(help_text="Data de nascimento do usuário", blank=False, null=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta(BaseModel.Meta):
        db_table = "usuario"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["matricula"]
        
    def __str__(self):
        return f"{self.user.first_name} - {self.matricula}"
    
class Curso(BaseModel):
    nome = models.CharField(help_text="Nome do curso", max_length=30, blank=False, null=False)

    class Meta(BaseModel.Meta):
        db_table = "curso"
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["nome"]
        
    def __str__(self):
        return self.nome
        
class Turma(BaseModel):
    nome = models.CharField(help_text="Nome da turma", max_length=5, blank=False, null=False)
    
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name="turmas", blank=False, null=False)
    
    ano = models.PositiveSmallIntegerField(help_text="Ano da turma", blank=False, null=False)
    
    class Meta(BaseModel.Meta):
        db_table = "turma"
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"
        ordering = ["nome"]
        
    def __str__(self):
        return self.nome

class Aluno(BaseModel):
    matricula = models.CharField(help_text="Matrícula do aluno", max_length=20, unique=True, db_index=True, blank=False, null=False)
    
    nome = models.CharField(help_text="Nome do aluno", max_length=70, blank=False, null=False)
    nascimento = models.DateField(help_text="Data de nascimento do aluno", blank=False, null=False)
    nome_responsavel = models.CharField(help_text="Nome do responsável pelo aluno", max_length=100, blank=False, null=False)
    peso = models.DecimalField(help_text="Peso do aluno", max_digits=5, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(help_text="Altura do aluno", max_digits=4, decimal_places=2, null=True, blank=True)
    medicamentos = models.TextField(help_text="Medicamentos contínuos consumidos pelo aluno", blank=True, null=True)
    restricoes = models.TextField(help_text="Restrições/Impedimentos médicos do aluno", blank=True, null=True)
    observacoes = models.TextField(help_text="Observações internas sobre o aluno", blank=True, null=True)
    
    TIPOS_SANGUINEOS = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
]
    tipo_sanguineo = models.CharField(help_text="Tipo sanguíneo do aluno", max_length=3, choices=TIPOS_SANGUINEOS, blank=True, null=True)
    
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT, blank=False, null=False)
    
    class Meta(BaseModel.Meta):
        db_table = "aluno"
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
        ordering = ["nome"]
        
    def __str__(self):
        return f"{self.nome} - ({self.matricula})"

class Prontuario(BaseModel):
    data = models.DateField(help_text="Data do prontuário", blank=False, null=False)
    horario_inicio = models.TimeField(help_text="Horário de ínicio do prontuário", blank=False, null=False)
    horario_fim = models.TimeField(help_text="Horário de fim do prontuário", blank=False, null=False)
    descricao = models.TextField(help_text="Descrição do prontuário", blank=False, null=False)
    
    TIPOS_ATENDIMENTO = [
    ("consulta", "Consulta"),
    ("urgencia", "Urgência"),
    ("medicacao", "Medicação"),
    ("retorno", "Retorno"),
]
    tipo_atendimento = models.CharField(help_text="Tipo de atendimento do prontuário", max_length=20, choices=TIPOS_ATENDIMENTO, db_index=True, blank=False, null=False)
    
    STATUS_ATENDIMENTO = [
    ("aberto", "Aberto"),
    ("finalizado", "Finalizado"),
    ("encaminhado", "Encaminhado"),
]
    status = models.CharField(help_text="Status do prontuário", max_length=20, choices=STATUS_ATENDIMENTO, db_index=True, blank=False, null=False)
    
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT, related_name="prontuarios", blank=False, null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name="prontuarios", blank=False, null=True)
    
    class Meta(BaseModel.Meta):
        db_table = "prontuario"
        verbose_name = "Prontuário"
        verbose_name_plural = "Prontuários"
        ordering = ["-data"]
        
    def __str__(self):
        return f"Prontuário #{self.id}"

class Declaracao(BaseModel):
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, help_text="Código da Declaracão", unique=True, blank=False, null=False)

    descricao = models.TextField(help_text="Descrição da Declaracão", blank=False, null=False)
    observacoes_internas = models.TextField(help_text="Observações próprias do(a) responsável pela declaracão", blank=True, null=True)
    
    prontuario = models.OneToOneField(Prontuario, on_delete=models.PROTECT, primary_key=True, related_name="declaracoes", blank=False, null=False)
    emitido_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, related_name="declaracoes_emitidas", null=True)
    data_horario_emissao = models.DateTimeField(auto_now_add=True)  
    
    class Meta(BaseModel.Meta):
        db_table = "declaracao"
        verbose_name = "Declaração"
        verbose_name_plural = "Declarações"
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"Declaração - {self.codigo}"