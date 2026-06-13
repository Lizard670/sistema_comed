from django import forms
from .models import Aluno
from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Div, HTML, Reset, Submit


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