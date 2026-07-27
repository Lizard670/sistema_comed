from django.shortcuts import get_object_or_404, render
from core.models import Prontuario

from . import forms 

def pagina_inicial(request):
    return render(request, "index.html")

def pagina_logar(request):
    if request.method == "POST":
        print(request)
        form = forms.Login(request.POST)
        if form.is_valid():
            # TODO: Validar os dados do usuário e logar caso estejam certos
            pass

    else:
        form = forms.Login()

    return render(request, "logar.html", {"form": form})

def pagina_registrar(request):
    return render(request, "registrar.html")

def pagina_resetar_senha(request):
    return render(request, "resetar_senha.html")

def pagina_estudantes(request):
    if request.method == "POST":
        print(request)
        form = forms.Estudante(request.POST)
        if form.is_valid():
            # TODO: Criar um novo prontuário no banco de dados usando as informações do forms
            pass

    else:
        form = forms.Estudante()

    return render(request, "estudantes.html", {"form": form})

def pagina_prontuario(request, pk=None):
    prontuario = get_object_or_404(Prontuario, pk=pk) if pk is not None else None

    if request.method == "POST":
        print(request)
        form = forms.Prontuario(request.POST)
        if form.is_valid():
            # TODO: Criar um novo prontuário no banco de dados usando as informações do forms
            pass

    else:
        valores_iniciais = {}
        if prontuario:
            valores_iniciais = {
                "paciente": prontuario.aluno_id,
                "data": prontuario.data,
                "inicio": prontuario.horario_inicio,
                "fim": prontuario.horario_fim,
                "descricao": prontuario.descricao,
            }
        form = forms.Prontuario(initial=valores_iniciais)

    return render(request, "prontuario.html", {"form": form, "prontuario": prontuario})
