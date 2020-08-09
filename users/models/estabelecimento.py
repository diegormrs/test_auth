# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

#import for the signal creation
from django.db.models.signals import post_save
from django.dispatch import receiver


#model que salva os dados do estabelecimento
#esse model é usado como o meio de ligação de todos os demais itens do sistema
#em vez de usar um usuario, o estabelecimnto é utilizado o que facilita multi-user
#por exemplo, ao se criar uma nova categoria, ela precisa ter um estabelecimento
#de maneira que pode ser usada por todos os usuários daquele estabelecimento

class Estabelecimento(models.Model):

############################################################################################################
############################################################################################################

    #deleta o estabelecimento se o usuário dono for deletado
    dono = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nome = models.CharField(max_length=100, unique=True)

############################################################################################################
############################################################################################################

    class Meta:

        app_label = 'users'
        db_table = "estabelecimento"
        verbose_name = "Estabelecimento"
        unique_together = ("dono", "nome")

        permissions = (
            ("estabelecimento", "Estabelecimento"),
        )

############################################################################################################
############################################################################################################

    def __str__(self):
        return str(self.nome)

############################################################################################################
############################################################################################################
