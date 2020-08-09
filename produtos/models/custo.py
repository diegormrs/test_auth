# -*- coding: UTF-8 -*-

from django.core.validators import MinValueValidator
from django.db import models

from users.models import Estabelecimento


#custo é utilizado para agregar valores ao produto
#como custo de energia, desperdicio, importos
#e quaisquer custos que possam afetar o preco do produto



class Custo(models.Model):

    #determina o tipo de custo
    tipo = (('porcentagem', 'Porcentagem'),
            ('real', 'Real'))

    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    tipo = models.CharField(choices=tipo, default='porcentagem', max_length=11)
    valor = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)], default=None, null=True)
    nome = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'produtos'
        db_table = 'custo'
        verbose_name = "Custo"
        unique_together = ("estabelecimento", "nome")

############################################################################################################
############################################################################################################

    def __str__(self):

        if self.tipo == 'porcentagem':
            return str(self.nome) + " - " + str(self.valor) +"%"
        else:
            return str(self.nome) + " - " + str(self.valor) +"R$"

############################################################################################################
############################################################################################################