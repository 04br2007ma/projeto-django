from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from projeto.usuarios.models import Usuario
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from projeto.area_administrativa.models import  Musculo, DiaSemana, SemanaTreino, TreinoDia, Dieta  
from django.http import HttpResponseBadRequest
from datetime import date, timedelta
import json

hoje = date.today()
ano, semana, dia_da_semana = hoje.isocalendar()

def inicio_semana(d):
    return d - timedelta(days=d.weekday())

def fim_semana(d):
    return inicio_semana(d) + timedelta(days=6)


@login_required
def painel_dashboard(request):
    usuario = request.user

    # Semanas recentes (3 últimas)
    semanas_recentes = SemanaTreino.objects.filter(
        user=usuario
    ).order_by("-inicio")[:3]

    # Dados para o gráfico
    semanas_graf = SemanaTreino.objects.filter(
        user=usuario
    ).order_by("inicio")[:10]

    graf_labels = [f"{s.inicio.strftime('%d/%m')}" for s in semanas_graf]
    graf_dados = [TreinoDia.objects.filter(semana=s).count() for s in semanas_graf]

    return render(request, "painel_dashboard.html", {
        "usuario": usuario,
        "semanas_recentes": semanas_recentes,
        "graf_labels": graf_labels,
        "graf_dados": graf_dados,
    })


@login_required
def meu_perfil(request):
    usuario = request.user  
    treino = SemanaTreino.objects.filter(user=request.user)
    return render(request, "index-meu-perfil.html", {"treino": treino,"usuario": usuario})


@login_required
def editar_perfil(request):
    usuario = request.user

    if request.method == "POST":
        usuario.first_name = request.POST.get("first_name")
        usuario.last_name = request.POST.get("last_name")
        usuario.email = request.POST.get("email")
        usuario.bio = request.POST.get("bio")

        if request.FILES.get("avatar"):
            usuario.avatar = request.FILES["avatar"]

        usuario.save()
        return redirect("painel_dashboard")  


    return render(request, "usuarios/editar_perfil.html", {
        "usuario": usuario
    })


@login_required
def trocar_senha(request):
    usuario = request.user    
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("painel_dashboard")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "usuarios/trocar_senha.html", {"form": form, "usuario": usuario})


@login_required
def meus_treinos(request):
    usuario = request.user

    # =============================
    # 1) DEFINIR SEMANA ATUAL
    # =============================
    hoje = date.today()
    inicio_semana = hoje - timedelta(days=hoje.weekday())   # segunda
    fim_semana = inicio_semana + timedelta(days=6)          # domingo

    # get_or_create garante que sempre exista UMA semana atual
    semana_atual, _ = SemanaTreino.objects.get_or_create(
        user=usuario,
        inicio=inicio_semana,
        fim=fim_semana
    )

    # =============================
    # 2) BUSCAR SEMANA PELO PARÂMETRO
    # =============================
    param = request.GET.get("semana")

    if param:
        # formato: "2025-48"
        ano, semana_num = param.split("-")
        ano = int(ano)
        semana_num = int(semana_num)

        # converter ISO week → data real
        inicio_escolhida = date.fromisocalendar(ano, semana_num, 1)  # segunda
        fim_escolhida = inicio_escolhida + timedelta(days=6)         # domingo

        semana = SemanaTreino.objects.filter(
            user=usuario,
            inicio=inicio_escolhida,
            fim=fim_escolhida
        ).first()
    else:
        # DEFAULT: mostrar a semana atual
        semana = semana_atual

    # =============================
    # 3) TREINOS DO DIA
    # =============================
    treino_dias = (
        TreinoDia.objects
        .filter(semana=semana)
        .select_related("dia")
        .prefetch_related("musculos")
    )

    # =============================
    # 4) HISTÓRICO COMPLETO
    # =============================
    semanas = (
        SemanaTreino.objects
        .filter(user=usuario)
        .order_by("-inicio")
    )

    semanas_passadas = semanas.filter(inicio__lt=inicio_semana)
    semanas_futuras = semanas.filter(inicio__gt=inicio_semana)

    return render(request, "meus-treinos/index-meus-treinos.html", {
        "semanas": semanas,
        "semana": semana,
        "treino_dias": treino_dias,
        "semana_atual": semana_atual,
        "semanas_passadas": semanas_passadas,
        "semanas_futuras": semanas_futuras,
        "usuario":usuario
    })



@login_required
def detalhe_semana(request, semana_id):
    semana = get_object_or_404(SemanaTreino, id=semana_id, user=request.user)
    treinos = TreinoDia.objects.filter(semana=semana).order_by("dia__id")

    return render(request, "meus-treinos/detalhe_semana.html", {
        "semana": semana,
        "treinos": treinos
    })


@login_required
def semanas(request):
    semanas = SemanaTreino.objects.filter(user=request.user).order_by("-inicio")
    return render(request, "semanas/listar.html", {"semanas": semanas})


def criar_treino_semana(request):
    usuario = request.user
    dias = DiaSemana.objects.all().order_by('id')
    musculos = Musculo.objects.all().order_by('nome')

    return render(request, "treinos/criar_novo_treino.html", {
            "dias": dias,
            "musculos": musculos,
            "usuario": usuario
        })


@login_required
def criar_semana_atual(request):
    hoje = date.today()
    inicio = inicio_semana(hoje)
    fim = fim_semana(hoje)

    semana, criada = SemanaTreino.objects.get_or_create(
        user=request.user,
        inicio=inicio,
        defaults={"fim": fim}
    )
    return redirect("editar_semana", semana.id)

@login_required
def editar_semana(request, semana_id):
    usuario = request.user  
    if request.method == "GET":
        selecao = request.GET.get("selecao")

        if not selecao:
            return HttpResponseBadRequest("Nenhuma seleção recebida.")

        mapa = {}
        partes = selecao.split(";")

        for p in partes:
            dia, muscs = p.split(":")
            dia = int(dia)
            ids = [int(x) for x in muscs.split(",") if x]
            mapa[dia] = ids

        dias = DiaSemana.objects.filter(id__in=mapa.keys())
        musculos = Musculo.objects.filter(id__in=[m for lista in mapa.values() for m in lista])

        # transforma para acessar com mapa_list.dia_id
        mapa_list = {}
        for d in dias:
            mapa_list[d.id] = mapa.get(d.id, [])

        return render(request, "treinos/confirmar_treino.html", {
            "dias": dias,
            "musculos": musculos,
            "mapa": mapa_list,
            "selecao": selecao,
            "usuario":usuario
        })


    # POST -> salva peso e os músculos por dia
    if request.method == "POST":
        # salvar peso
        peso_raw = request.POST.get("peso", "").strip()
        if peso_raw:
            try:
                semana.peso = int(peso_raw)
            except ValueError:
                return HttpResponseBadRequest("Peso inválido.")
        else:
            semana.peso = None
        semana.save()

        # salvar músculos por dia
        for key, value in request.POST.items():
            if not key.startswith("dia_"):
                continue
            try:
                dia_id = int(key.split("_", 1)[1])
            except (IndexError, ValueError):
                continue

            ids = [int(x) for x in value.split(",") if x.strip()]
            treino_dia, _ = TreinoDia.objects.get_or_create(semana=semana, dia_id=dia_id)
            treino_dia.musculos.set(ids)

        return redirect("semanas")

@login_required
def escolher_musculos(request):
    usuario = request.user  
    musculos = Musculo.objects.all()
    print(musculos)
    return render(request, "treinos/escolher_musculos.html", {
        "musculos": musculos,
        "usuario": usuario
    })

@login_required    
def escolher_dias(request):
    usuario = request.user  
    musculos_ids = request.GET.get("musculos")

    if not musculos_ids:
        return HttpResponseBadRequest("Nenhum músculo selecionado.")

    lista_ids = musculos_ids.split(",")
    musculos = Musculo.objects.filter(id__in=lista_ids)

    dias = DiaSemana.objects.all()

    return render(request, "treinos/escolher_dias.html", {
        "musculos": musculos_ids,            # ids para passar adiante
        "nomes_musculos": ", ".join(m.nome for m in musculos),
        "dias": dias,
        "usuario": usuario
    })

@login_required
def confirmar_treino(request):
    usuario = request.user 
    if request.method == "GET":
        selecao = request.GET.get("selecao")

        if not selecao:
            return HttpResponseBadRequest("Nenhuma seleção recebida.")

        mapa = {}
        partes = selecao.split(";")

        for p in partes:
            dia, muscs = p.split(":")
            dia = int(dia)
            ids = [int(x) for x in muscs.split(",") if x]
            mapa[dia] = ids

        dias = DiaSemana.objects.filter(id__in=mapa.keys())
        musculos = Musculo.objects.filter(id__in=[m for lista in mapa.values() for m in lista])

        # MANDAR O MAPA COMO UM OBJETO JSON-READY PARA O TEMPLATE
        mapa_json = json.dumps(mapa)

        return render(request, "treinos/confirmar_treino.html", {
            "mapa": mapa,
            "mapa_json": mapa_json,
            "dias": dias,
            "musculos": musculos,
            "selecao": selecao,
            "usuario": usuario
        })
    # POST -> salvar
    if request.method == "POST":
        selecao = request.POST.get("selecao")
        treino_json = json.loads(request.POST.get("treino_json"))

        if not selecao:
            return HttpResponseBadRequest("Nenhum dado recebido no POST.")

        partes = selecao.split(";")

        hoje = date.today()
        inicio = hoje - timedelta(days=hoje.weekday())
        fim = inicio + timedelta(days=6)

        semana = SemanaTreino.objects.create(
            user=request.user,
            inicio=inicio,
            fim=fim
        )

        for p in partes:
            if ":" not in p:
                continue

            dia, muscs = p.split(":")
            dia = int(dia)
            musc_ids = [int(x) for x in muscs.split(",") if x]

            treino_dia = TreinoDia.objects.create(
                semana=semana,
                dia_id=dia
            )
            treino_dia.musculos.set(musc_ids)

        return redirect("meu_perfil")

@login_required
def montar_treino(request):
    if request.method == "POST":
        treino = []#TreinoSemana.objects.filter(user=request.user).delete()  # limpa treino antigo
        
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