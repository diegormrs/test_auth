# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.models import User
from pedido.models.pedido import Pedido

class PedidoFinalizarForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # must use the estabelecimento id in the init, to test the unique_together after on the clean methods
        #self.estabelecimentoid = kwargs.pop('estabelecimentoid')
        #self.userid = kwargs.pop('pedidoid')

        super(PedidoFinalizarForm, self).__init__(*args, **kwargs)

############################################################################################################
############################################################################################################
    def save(self, commit=True):
        #need to update the order to complete, then after the signal can calculate the value
        self.instance.pedidocompleto = True
        return super(PedidoFinalizarForm, self).save()

    class Meta:
        model = Pedido
        fields = ['dataentrega', 'entrega', 'embalagem', 'desconto', 'acrescimo', 'observacoes']