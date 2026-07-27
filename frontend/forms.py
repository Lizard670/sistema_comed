from django import forms
from core.models import Aluno, Turma
from datetime import date


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Div, HTML, Reset, Submit



class Login(forms.Form):
    email = forms.EmailField(label="Endereço de email",
                             widget=forms.EmailInput())
    senha = forms.CharField(label="senha",
                            widget=forms.PasswordInput())
    lembrar = forms.BooleanField(label="Manter conectado",
                                 widget=forms.CheckboxInput,
                                 required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Div(
                'email',
            css_class="form-floating mb-3"),
            Div(
                'senha',
            css_class="form-floating mb-3"),
            Div( 
                'lembrar',
            css_class="form-check mb-3"),
            Div( 
                HTML("<a class=\"small\" href=\"{% url 'resetar_senha' %}\">Esqueci a senha</a>"),
                Submit('login', 'Entrar', css_class='btn btn-primary'),
            css_class="d-flex align-items-center justify-content-between mt-4 mb-0"),
        )


class Prontuario(forms.Form):
    paciente = forms.ModelChoiceField(label="Paciente", 
                                      queryset=Aluno.objects.all())
    data = forms.DateField(label="Data da consulta", 
                           initial=date.today, 
                           widget=forms.DateInput(attrs={'type': 'date'}))
    
    inicio = forms.TimeField(label="Horário início", 
                             widget=forms.TimeInput(attrs={'type': 'time'}))
    fim = forms.TimeField(label="Horário fim", 
                             widget=forms.TimeInput(attrs={'type': 'time'}))
    
    descricao = forms.CharField(label="",
                                widget=forms.Textarea())
    
    declaracao = forms.CharField(label="",
                                 widget=forms.Textarea())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Div('paciente', css_class="col-xl-8"),
            css_class="row"),

            Div(
                Div('data', css_class="col-xl-2"),
                Div('inicio', css_class="col-xl-2"),
                Div('fim', css_class="col-xl-2"),
            css_class="row"),

            HTML('<h3>Descrição interna</h1>'),
            'descricao',

            HTML('<h3>Texto declaração</h1>'),
            'declaracao',

            Button('declaracao', 'Gerar declaração', css_class='btn-secondary'),
            Reset('limpar', 'Limpar', css_class='btn-danger'),
            Submit('salvar', 'Salvar', css_class='btn-success')
        )



class Estudante(forms.Form):
    nome = forms.ModelChoiceField(label="Aluno", 
                                      queryset=Aluno.objects.all())
    data = forms.DateField(label="Data de nascimento",                        
                           widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    mae = forms.CharField(label="Nome da mãe",
                          required=False)

    peso = forms.FloatField(label="Peso",
                            required=False)

    altura = forms.FloatField(label="Altura",
                              required=False)

    matricula = forms.IntegerField(label="Matrícula")

    turma = forms.ChoiceField(label="Turma" ,
                              widget=forms.Select(), required=False)
    
    tipo = forms.ChoiceField(label="Tipo Sanguíneo", 
                             widget=forms.Select(), required=False)
    
    descricao = forms.CharField(label="",
                                widget=forms.Textarea(), required=False)
    
    restricoes = forms.CharField(label="Restrições",
                                 widget=forms.Textarea(), required=False)
    
    medicamentos = forms.CharField(label="Medicamentos contínuos",
                                 widget=forms.Textarea(), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Os valores também são usados pelo JavaScript quando um aluno é
        # selecionado na tabela. Sem essas opções, definir ``select.value``
        # não produz nenhum valor visível no formulário.
        self.fields["turma"].choices = [("", "Selecione uma turma")] + [
            (turma.pk, turma.nome) for turma in Turma.objects.select_related("curso")
        ]
        self.fields["tipo"].choices = [("", "Selecione o tipo sanguíneo")] + list(
            Aluno.TIPOS_SANGUINEOS
        )

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Div(
                Div('nome', css_class="col-xl-8"),
            css_class="row"),

            Div(
                Div('data', css_class="col-xl-2"),
                Div('tipo', css_class="col-xl-2"),
                Div('peso', css_class="col-xl-2"),
                Div('mae', css_class="col-xl-3"),

               
            css_class="row justify-content-between"),

            Div(
                Div('altura', css_class="col-xl-2"),
                Div('matricula', css_class="col-xl-2"),
                Div('turma', css_class="col-xl-2"),
                
                

            css_class="row justify-content-between"),
            
            
           
            
            
                

            

            

            HTML('<h3>Observações</h1>'),
            'descricao',
            
            
         Div(
                Div('restricoes', css_class="col-xl-5"),
                Div('medicamentos', css_class="col-xl-5"),

            css_class="row justify-content-between"),   
            
            
            
            


            
            


            Reset('limpar', 'Limpar', css_class='btn-danger'),
            Submit('salvar', 'Salvar', css_class='btn-success')
        )
