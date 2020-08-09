# -*- coding: UTF-8 -*-

from django.core.validators import MinValueValidator
from django.db import models

# model que salva os dados do estabeleicmentos de venda
# por exemplo, mercdo livre, elo7 ou mesmo serve para salvar a taxa do cartão de crédito
from users.models import Estabelecimento


class CanalVenda(models.Model):

    estabelecimento = models.ForeignKey(Estabelecimento,  on_delete=models.CASCADE)
    porcentagem = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.00)], default=0)
    nome = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'produtos'
        db_table = 'canalvenda'
        verbose_name = "Canal de Venda"
        unique_together = ("estabelecimento", "nome")

############################################################################################################
############################################################################################################

    def __str__(self):

        return self.nome + " | " + str(self.porcentagem)

###########################################################################################################
###########################################################################################################
