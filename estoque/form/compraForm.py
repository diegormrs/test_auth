# -*- coding: UTF-8 -*-

from django import forms

from estoque.models.compra import Compra
from produtos.models.custo import Custo

class CompraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #must use the estabelecimento id in the init, to test the unique_together after on the clean methods
        self.estabelecimentoid = kwargs.pop('estabelecimentoid')

        super(CompraForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Compra
        exclude = ['user', 'estabelecimento', 'data', 'precounitario']