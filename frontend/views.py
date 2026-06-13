from django.shortcuts import render

from . import forms 

def pagina_inicial(request):
    return render(request, "index.html")

def pagina_logar(request):
    return render(request, "logar.html")

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

def pagina_prontuario(request):
    if request.method == "POST":
        print(request)
        form = forms.Prontuario(request.POST)
        if form.is_valid():
            # TODO: Criar um novo prontuário no banco de dados usando as informações do forms
            pass

    else:
        form = forms.Prontuario()

    return render(request, "prontuario.html", {"form": form})