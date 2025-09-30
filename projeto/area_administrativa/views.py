from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home_administrativo(request):
    return render(request, "index-area-restrita.html")


def meus_treinos_foda(request):
   return render(request, "meus-treinos/index-meu-treino.html")
