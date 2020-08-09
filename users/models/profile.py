# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from users.models.estabelecimento import Estabelecimento

from django.db.models.signals import post_save
from django.dispatch import receiver

#model que cria o link entre múltiplos usuários e um estabelecimento
#em caso de necessidade de adicionar mais dados a um usuário, esse é o model a ser usado

class Profile(models.Model):

############################################################################################################
############################################################################################################

    #deleta o estabelecimento se o usuário dono for deletado
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    celular = models.CharField(max_length=11)

############################################################################################################
############################################################################################################

    class Meta:

        app_label = 'users'
        db_table = "profile"
        verbose_name = "Profile"

        permissions = (
            ("profile", "Profile"),
        )

############################################################################################################
############################################################################################################

    def __str__(self):
        return str(self.user.email +" | "+ self.estabelecimento.nome)

############################################################################################################
############################################################################################################
