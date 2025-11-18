from django.shortcuts import render, redirect
from .models import TreinoSemana
from django.contrib.auth.decorators import login_required

# from .models import Pessoa

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

@login_required
def meu_perfil(request):
    treino = TreinoSemana.objects.filter(user=request.user)
    return render(request, "perfil.html", {"treino": treino})


def escolher_dias(request):
    musculos = request.GET.get("musculos", "").split(",")

    dias_semana = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]

    return render(request, "escolher_dias.html", {
        "musculos": musculos,
        "dias": dias_semana
    })



@login_required
def montar_treino(request):
    if request.method == "POST":
        treino = TreinoSemana.objects.filter(user=request.user).delete()  # limpa treino antigo
        
        dia_valor = request.get.POST("")
        for key, value in request.POST.items():
            if key.startswith("dia_"):
                musculo = key.replace("dia_", "")
                TreinoSemana.objects.create(
                    user=request.user,
                    dia=value,
                    musculos=musculo
                )

        return redirect("meu_perfil")  # redireciona ao perfil

    return redirect("inicio")


# def lista_pessoas(request):
#     pessoas = Pessoa.objects.all().order_by('nome')
#     return render(request, 'pessoas.html', {'pessoas': pessoas})