from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from datetime import date, timedelta

hoje = date.today()
ano, semana, dia_da_semana = hoje.isocalendar()


# Create your views here.
def home(request):
    return render(request, 'index.html')

def contato(request):
    nome = 'MATHEUS'
    line = '50'
    return render(request, 'proxpag.html',{'nome': nome,'line': line})

def dieta(request):
    return render(request, 'dieta.html')

def cronograma(request):
    return render(request, 'cronograma.html')

def musculos(request):
    return render(request, 'musculos.html')

def cargas(request):
    return render(request, 'cargas.html')


def meu_perfil(request):
    return render(request, 'meu_perfil.html')

