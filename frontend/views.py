from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from . import forms 

@login_required
def pagina_inicial(request):
    print("-"*10)
    print(request.user)
    return render(request, "index.html")

def pagina_deslogar(request):
    logout(request)
    return redirect(reverse("login"))

@login_required
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

@login_required
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