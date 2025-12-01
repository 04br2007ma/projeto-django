from django.db import models
from django.conf import settings


# Create your models here.

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)


class Dieta(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome
    

class Musculo(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='musculos/', null=True, blank=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class DiaSemana(models.Model):
    nome = models.CharField(max_length=13)
    sigla = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.nome

class SemanaTreino(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    inicio = models.DateField()      # segunda-feira
    fim = models.DateField()         # domingo
    numero_semana = models.PositiveSmallIntegerField()
    peso = models.PositiveSmallIntegerField(
        verbose_name="peso atual",
        null=True,
        blank=True
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'inicio', 'fim')
        
    @property
    def numero_semana(self):
        return self.inicio.isocalendar()[1]

    @property
    def ano(self):
        return self.inicio.isocalendar()[0]

    def __str__(self):
        return f"{self.user} - Semana {self.numero_semana}/{self.ano}"



class TreinoDia(models.Model):
    semana = models.ForeignKey(SemanaTreino, on_delete=models.CASCADE, related_name="treinos")
    dia = models.ForeignKey(DiaSemana, on_delete=models.CASCADE)
    musculos = models.ManyToManyField(Musculo)

    def __str__(self):
        return f"{self.semana} - {self.dia}"
