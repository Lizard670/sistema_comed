from django.shortcuts import render

def pagina_inicial(request):
    return render(request, "index.html")

def pagina_logar(request):
    return render(request, "logar.html")

def pagina_registrar(request):
    return render(request, "registrar.html")

def pagina_resetar_senha(request):
    return render(request, "resetar_senha.html")