
# -*- coding: UTF-8 -*-

from decimal import Decimal, ROUND_DOWN

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from produtos.models.materiaprima import MateriaPrima
from users.models import Estabelecimento


class Perda(models.Model):

    materia = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True)
    quantidade = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

############################################################################################################
############################################################################################################

    class Meta:
        app_label = 'estoque'
        db_table = 'perda'

############################################################################################################
############################################################################################################

    def __str__(self):

        return str(self.materia.nome + " | " + str(self.quantidade))

############################################################################################################
############################################################################################################