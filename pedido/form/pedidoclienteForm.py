# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.models import User
from pedido.models.pedido import Pedido

class PedidoClienteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #must use the estabelecimento id in the init, to test the unique_together after on the clean methods
        self.estabelecimentoid = kwargs.pop('estabelecimentoid')
        self.userid = kwargs.pop('userid')

        super(PedidoClienteForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        #need to add the user before saving
        m = super(PedidoClienteForm, self).save(commit=False)
        m.user = User.objects.get(id=self.userid)
        #set to complete the first step of the order
        m.pedidoclientecompleto = True
        m.save()
        return m

    class Meta:
        model = Pedido
        fields = ['cliente', 'canalvenda', 'status']