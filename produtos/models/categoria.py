# -*- coding: utf-8 -*-

from django.db import models

# categorias são utilizadas para separar as materias-primas em grupos
# é utilizado para dividiar as materias na tela de cadastro de produto em abas
from users.models import Estabelecimento


class Categoria(models.Model):

    nome = models.CharField(max_length=30)
    ativo = models.BooleanField(default=True)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'produtos'
        db_table = "categoria"
        verbose_name = "Categoria"
        unique_together = ("estabelecimento", "nome")

        ordering = ['nome', '-ativo']

        permissions = (
            ("categorias", "Categorias"),
        )

############################################################################################################
############################################################################################################

    def __str__(self):

        return self.nome

############################################################################################################
############################################################################################################
