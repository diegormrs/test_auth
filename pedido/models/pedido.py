# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from pedido.models.cliente import Cliente
from pedido.models.pedidoproduto import PedidoProduto
from produtos.models.canalvenda import CanalVenda
from users.models import Estabelecimento


class Pedido(models.Model):

    #determina o status do pedido
    status = (('orcamento', 'Orçamento'),
            ('producao', 'Em produção'),
             ('entregue', 'Entregue'))

    data = models.DateTimeField(auto_now=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    canalvenda = models.ForeignKey(CanalVenda, on_delete=models.CASCADE)
    dataentrega = models.DateField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    produtos = models.ManyToManyField(to='produtos.produto', through=PedidoProduto)

    valor = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)], default=None, null=True)
    entrega = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], default=0)
    embalagem = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], default=0)
    desconto = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], default=0)
    acrescimo = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)], default=0)

    observacoes = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(choices=status, default='orcamento', max_length=11)

    pedidoclientecompleto = models.BooleanField(default=False)
    pedidoprodutoscompleto = models.BooleanField(default=False)
    pedidocompleto = models.BooleanField(default=False)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'pedido'
        db_table = "pedido"

############################################################################################################
############################################################################################################

    def __str__(self):

        return self.cliente.nome

    def is_completo(self):

        return (self.pedidoclientecompleto and self.pedidoprodutoscompleto and self.pedidocompleto)

############################################################################################################
############################################################################################################
