from django.contrib import admin

# Register your models here.
from projeto.area_administrativa.models import  Musculo, DiaSemana, SemanaTreino, TreinoDia#, Dieta  


admin.site.register(Musculo)
admin.site.register(DiaSemana)
admin.site.register(SemanaTreino)
admin.site.register(TreinoDia)
# admin.site.register(Dieta)