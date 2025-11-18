from django.urls import path
from . import views

urlpatterns = [
    path ('',views.home, name='home'),
    path('proxpag/',views.contato,name='proxpag'),
    path('dieta/', views.dieta, name='dieta'),
    path('cronograma/', views.cronograma, name='cronograma'),
    path('musculos/', views.musculos, name='musculos'),
    path('meu_perfil/', views.meu_perfil, name='meu_perfil'),
    path('cargas/', views.cargas, name='cargas'),
    path('escolher-dia/', views.escolher_dias, name='escolher_dias'),
    path('montar-treino/', views.montar_treino, name='montar_treino'),

    

    # path('pessoas/', views.lista_pessoas, name='lista_pessoas'),
]