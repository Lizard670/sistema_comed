from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Aluno, Turma, Curso

admin.site.register(Aluno)
admin.site.register(Turma)
admin.site.register(Curso)
