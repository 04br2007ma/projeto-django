from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projeto.usuarios.models import Usuario
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required
def home_administrativo(request):
    usuario = get_object_or_404(Usuario, username=request.user.username)
    print(usuario.avatar)
    return render(request, "index-area-restrita.html", {"usuario": usuario})


def meus_treinos_foda(request):
   return render(request, "meus-treinos/index-meu-treino.html")
