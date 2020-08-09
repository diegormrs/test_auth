# -*- coding: UTF-8 -*-

from django import forms

from estoque.models.compra import Compra
from estoque.models.estoque import Estoque
from estoque.models.perda import Perda
from produtos.models.custo import Custo

class PerdaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #must use the estabelecimento id in the init, to test the unique_together after on the clean methods
        self.estabelecimentoid = kwargs.pop('estabelecimentoid')

        super(PerdaForm, self).__init__(*args, **kwargs)

    def clean(self):
        #need to check if the materi-prima lose, it'' not bigger than the stock
        cleaned_data = self.cleaned_data

        #if there is no stock, there is no way to create a perda
        try:
            estoque  = Estoque.objects.get(materia=cleaned_data['materia'].id)
        except Exception as e:
            raise forms.ValidationError("A Matéria-Prima seleciona ainda não existe no Estoque. Não pode cadastrar uma Perda.")

        #if the perda is bigger than the stock value, it's not possible to creat it
        if estoque.quantidade < cleaned_data['quantidade']:
            raise forms.ValidationError("A Perda não pode ser maior do que a quantidade existente no Estoque. "
                                        "O valor do estoque atual é: " + str(estoque.quantidade))

        return cleaned_data

    class Meta:
        model = Perda
        exclude = ['user', 'estabelecimento', 'data']