# -*- coding: UTF-8 -*-

from django import forms

from produtos.models.materiaprima import MateriaPrima


class MateriaPrimaForm(forms.ModelForm):

    class Meta:
        model = MateriaPrima
        exclude = ['ativo', 'estabelecimento']