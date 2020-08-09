# -*- coding: UTF-8 -*-

from django.core.validators import MinValueValidator
from django.db import models

from produtos.models.canalvenda import CanalVenda
from produtos.models.produto import Produto
from users.models import Estabelecimento


#this is how the price is calculate
# 1 - sum all the materias * quantidade
# 2 - add all the custo in dinheiro
# 3 - add all the custo in porcentagem preco = preco * (1 + porcentagem/100)
# 4 - then add the value of the canal de venda
# 5 - save one price for each canal venda

class Preco(models.Model):

    preco = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    canalvenda = models.ForeignKey(CanalVenda, on_delete=models.CASCADE)
    datainicio = models.DateTimeField(auto_now=True)
    datafim = models.DateTimeField(blank=True, null=True)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = "produtos"
        db_table = "preco"
        verbose_name = "Preço"