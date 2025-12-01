from django.urls import path
from . import views

urlpatterns = [
    path("", views.painel_dashboard, name="painel_dashboard"),
    path('usuario/', views.meu_perfil, name='meu_perfil'),
    path("usuario/trocar-senha/", views.trocar_senha, name="trocar_senha"),

    path("editar-perfil/", views.editar_perfil, name="editar_perfil"),

    path('meus-treinos/', views.meus_treinos, name='meus_treinos'),
    path('meus-treinos/<int:semana_id>/', views.detalhe_semana, name='detalhe_semana'),
    path('meus-treinos/<int:semana_id>/', views.meus_treinos, name='meus_treinos'),
    
    path('montar-treino/', views.montar_treino, name='montar_treino'),

    path('treinos/criar-treino/', views.criar_treino_semana, name='criar_treino_semana'),    


    path('treinos/musculos/', views.escolher_musculos, name='escolher_musculos'),
    path('treinos/dias/', views.escolher_dias, name='escolher_dias'),
    path('treinos/confirmar/', views.confirmar_treino, name='confirmar_treino'),    

    path("semanas/", views.semanas, name="semanas"),
    path("semanas/atual/", views.criar_semana_atual, name="criar_semana_atual"),
    path("semanas/<int:semana_id>/editar/", views.editar_semana, name="editar_semana"),
    #path('criar-treino/', views.home_administrativo, name='home-administrativo'),
    
]


