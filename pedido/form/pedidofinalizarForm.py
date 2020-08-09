# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.models import User
from pedido.models.pedido import Pedido

class PedidoFinalizarForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ['dataentrega', 'entrega', 'embalagem', 'desconto', 'acrescimo', 'observacoes']