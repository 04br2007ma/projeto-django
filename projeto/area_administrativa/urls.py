from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_administrativo, name='home_administrativo'),
    path('meus-treinos-fodao/', views.meus_treinos_foda, name='meus_treinos'),

    #path('criar-treino/', views.home_administrativo, name='home-administrativo'),
    
]


