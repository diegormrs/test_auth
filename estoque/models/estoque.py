# -*- coding: UTF-8 -*-

from django.core.validators import MinValueValidator
from django.db import models

#salva os valores dos produtos comprados, baseados na média do valor das compras
from produtos.models.materiaprima import MateriaPrima
from users.models import Estabelecimento


class Estoque(models.Model):

    materia = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    quantidade = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    valor = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    valorunitario = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'estoque'
        db_table = 'estoque'

############################################################################################################
############################################################################################################

    def __str__(self):

        return str(self.materia.nome + " | " + str(self.quantidade))
