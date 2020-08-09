# -*- coding: UTF-8 -*-

from django.core.validators import MinValueValidator
from django.db import models



#salva os valores dos produtos comprados, baseados na média do valor das compras
from estoque.models.compra import Compra
from estoque.models.perda import Perda
from produtos.models.materiaprima import MateriaPrima
from users.models import Estabelecimento


class EstoqueHistorico(models.Model):

    materia = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)

    quantidadeantes = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    valorantes = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    valorunitarioantes = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    quantidadedepois = models.DecimalField(default=0, max_digits=12, decimal_places=4)
    valordepois = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    valorunitariodepois = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True)
    perda = models.ForeignKey(Perda, on_delete=models.CASCADE, null=True)

    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'estoque'
        db_table = 'estoque_historico'

############################################################################################################
############################################################################################################

    def __str__(self):

        return str(self.materia.nome + " | " + str(self.quantidade))
