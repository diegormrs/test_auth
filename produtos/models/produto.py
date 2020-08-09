# -*- coding: UTF-8 -*-

from django.core.validators import MinValueValidator
from django.db import models

from produtos.models.canalvenda import CanalVenda
from produtos.models.custo import Custo
from produtos.models.materiaprima import MateriaPrima
from produtos.models.produtomateria import ProdutoMateriaPrima
from users.models import Estabelecimento


class Produto(models.Model):

    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=300, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

    materiacompleto = models.BooleanField(default=False)
    canalcompleto = models.BooleanField(default=False)
    custocompleto = models.BooleanField(default=False)
    precocompleto = models.BooleanField(default=False)
    changed = models.BooleanField(default=False)
    updatepreco = models.BooleanField(default=False)

    canais = models.ManyToManyField(CanalVenda)
    custos = models.ManyToManyField(Custo)
    materias = models.ManyToManyField(MateriaPrima, through=ProdutoMateriaPrima)

    precobase = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)], default=None, null=True)
    lucro = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)], default=None, null=True)
############################################################################################################
############################################################################################################

    def __str__(self):

        return self.nome

############################################################################################################
###########################################################################################################

    def is_completo(self):

        return self.materiacompleto and self.canalcompleto and self.custocompleto and self.precocompleto

############################################################################################################
############################################################################################################

    def precolucro(self):

        return round( self.precobase * (1 + self.lucro/100),2)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'produtos'
        db_table = "produto"
        verbose_name = "Produto"

############################################################################################################
############################################################################################################