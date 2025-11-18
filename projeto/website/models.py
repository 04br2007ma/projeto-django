from django.db import models
from django.conf import settings


# Create your models here.

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)


class dieta(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome
    


class TreinoSemana(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dia = models.CharField(max_length=20)
    musculos = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user} - {self.dia}: {self.musculos}"

