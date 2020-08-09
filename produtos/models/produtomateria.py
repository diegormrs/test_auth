# -*- coding: UTF-8 -*-

from django.db import models

# salva as materias que compoe o produto
from produtos.models.materiaprima import MateriaPrima


class ProdutoMateriaPrima(models.Model):

    produto = models.ForeignKey(to='produtos.produto', on_delete=models.CASCADE)
    materiaprima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=16, decimal_places=2)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'produtos'
        db_table = "produtomateriaprima"

############################################################################################################
############################################################################################################

    def __str__(self):

        return self.produto.nome + " | " + self.materiaprima.nome + " - " + str(self.quantidade)

############################################################################################################
############################################################################################################
