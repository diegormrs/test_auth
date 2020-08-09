# -*- coding: UTF-8 -*-

from django import forms

from pedido.models.cliente import Cliente


class ClienteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #must use the estabelecimento id in the init, to test the unique_together after on the clean methods
        self.estabelecimentoid = kwargs.pop('estabelecimentoid')

        super(ClienteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Cliente
        exclude = ['ativo', 'estabelecimento']