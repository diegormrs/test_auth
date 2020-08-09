# -*- coding: utf-8 -*-

from django.db import models

from users.models import Estabelecimento


class Cliente(models.Model):
    UF_CHOICES = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MG', 'Minas Gerais'),
        ('MS', 'Mato Grosso do Sul'),
        ('MT', 'Mato Grosso'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PE', 'Pernanbuco'),
        ('PI', 'Piauí'),
        ('PR', 'Paraná'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('RS', 'Rio Grande do Sul'),
        ('SC', 'Santa Catarina'),
        ('SE', 'Sergipe'),
        ('SP', 'São Paulo'),
        ('TO', 'Tocantins')
    )
    #the user do not need to provide an address, just the name
    nome = models.CharField(max_length=200)
    ativo = models.BooleanField(default=True)
    telefone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(blank=True)
    cep = models.CharField(max_length=9, blank=True)
    estado = models.CharField(choices=UF_CHOICES, max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=200, blank=True)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'pedido'
        db_table = "cliente"

############################################################################################################
############################################################################################################

    def __str__(self):

        return self.nome

############################################################################################################
############################################################################################################
