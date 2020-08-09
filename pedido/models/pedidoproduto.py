# -*- coding: utf-8 -*-

from django.db import models

from produtos.models.produto import Produto


class PedidoProduto(models.Model):

    pedido = models.ForeignKey(to='pedido.pedido', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'pedido'
        db_table = "pedido_produto"

############################################################################################################
############################################################################################################
