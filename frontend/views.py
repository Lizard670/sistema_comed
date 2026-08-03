from django.shortcuts import render, redirect, get_object_or_404, render
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from . import forms 
from core.models import Prontuario, Declaracao, Usuario, Aluno

@login_required
def pagina_inicial(request):
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
def pagina_relatorios(request):
    form = forms.Relatorios()
    
    return render(request, "relatorios.html", {"form": form})

@login_required
def pagina_prontuario(request, pk=0, err=""):
    if request.method == "POST":
        form = forms.Prontuario(request.POST)
        if form.is_valid():
            if "salvar_prontuario" in request.POST:
                idPaciente = request.POST.get("paciente")
                paciente = Aluno.objects.get(id=idPaciente)
                data = request.POST.get("data")
                inicio = request.POST.get("inicio")
                fim = request.POST.get("fim")
                descricao = request.POST.get("descricao")
                status = request.POST.get("status")
                tipo_atendimento = request.POST.get("tipo_atendimento")
                
                if Prontuario.objects.filter(id=pk).exists():
                    prontuario = Prontuario.objects.get(id=pk)

                    prontuario.aluno = paciente
                    prontuario.data = data
                    prontuario.horario_inicio = inicio
                    prontuario.horario_fim = fim 
                    prontuario.descricao = descricao
                    prontuario.status = status
                    prontuario.tipo_atendimento = tipo_atendimento
                    
                    prontuario.save()
                else:
                    try:
                        usuario = Usuario.objects.get(user=request.user)
                    except Usuario.DoesNotExist as e:
                        return redirect(reverse("prontuario", kwargs={'pk':pk, 'err':403}))
                    
                    prontuario = Prontuario.objects.create(aluno=paciente, usuario=usuario,
                                                        data=data, horario_inicio=inicio, horario_fim=fim, 
                                                        descricao=descricao, status=status, tipo_atendimento=tipo_atendimento)

                return redirect(reverse("prontuario", kwargs={'pk':prontuario.id}))
            elif "salvar_declaracao" in request.POST and pk!=0:
                try:
                    usuario = Usuario.objects.get(user=request.user)
                except Usuario.DoesNotExist as e:
                    return redirect(reverse("prontuario", kwargs={'pk':pk, 'err':403}))
                
                descricao = request.POST.get("declaracao")
                
                if Declaracao.objects.filter(prontuario_id=pk).exists():
                    declaracao = Declaracao.objects.get(prontuario_id=pk)

                    declaracao.emitido_por = usuario
                    declaracao.descricao = descricao
                    declaracao.data_horario_emissao = now()
                    
                    declaracao.save()
                else:
                    declaracao = Declaracao.objects.create(prontuario_id=pk,
                                                           emitido_por=usuario, 
                                                           descricao=descricao, 
                                                           data_horario_emissao=now())

                return redirect(reverse("prontuario", kwargs={'pk':pk}))
        

    elif pk != 0:
        try:
            prontuario = Prontuario.objects.get(id=pk)
            initial = {
                'id': pk,
                'paciente': prontuario.aluno,
                'data': prontuario.data.strftime("%Y-%m-%d"),
                'inicio': prontuario.horario_inicio,
                'fim': prontuario.horario_fim,
                'status': prontuario.status,
                'tipo_atendimento': prontuario.tipo_atendimento,
                'descricao': prontuario.descricao
            }
            try:
                declaracao = Declaracao.objects.get(prontuario_id=pk)
                initial['declaracao'] = declaracao.descricao
            except Declaracao.DoesNotExist as e:
                print(f"- O Prontuário {pk} não possui declaração")
            form = forms.Prontuario(initial=initial)
            
        except Prontuario.DoesNotExist as e:
            return HttpResponseBadRequest()
    else:
        valores_iniciais = {}
        if pk!=0:
            valores_iniciais = {
                "paciente": prontuario.aluno_id,
                "data": prontuario.data,
                "inicio": prontuario.horario_inicio,
                "fim": prontuario.horario_fim,
                "descricao": prontuario.descricao,
            }
        form = forms.Prontuario(initial=valores_iniciais)

    return render(request, "prontuario.html", {"form": form, "pk": pk, "err": err})

def pagina_validar_declaracao(request, codigo=None):
    """Página pública para validar a autenticidade de uma declaração pelo código."""
    return render(request, "validar_declaracao.html", {"codigo": codigo})
