# -*- coding: UTF-8 -*-

from django import forms

from produtos.models.produto import Produto


class ProdutoLucroForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.estabelecimentoid = kwargs.pop('estabelecimentoid')
        self.produtoid = kwargs.pop('produtoid')

        super(ProdutoLucroForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Produto
        fields = ['lucro']