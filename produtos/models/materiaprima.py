# -*- coding: UTF-8 -*-

from django.db import models

# model das materias primas
# uilizado para compor os produtos
# cada matera prima é dmedida com um tipo de medida diferente
from produtos.models.categoria import Categoria
from users.models import Estabelecimento


class MateriaPrima(models.Model):

    medida = (
        ("un","Unidade"),
        ("gr", "Grama"),
        ("cm", "Centímetros"),
        ("ql", "Quilo"),
        ("ml", "Mililitro (ml)"),
        ("lt", "Litro"),
        ("cm2","Centímetro quadrado"),
        ("mt2", "Metro quadrado")
    )

    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=300, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    tipo_medida = models.CharField(choices=medida, default='un', max_length=3)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'produtos'
        db_table = "materiaprima"
        unique_together = ("nome", "categoria", "tipo_medida")

############################################################################################################
############################################################################################################

    def __str__(self):

        return self.nome + " | " + self.tipo_medida

############################################################################################################
############################################################################################################
