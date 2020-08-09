# -*- coding: UTF-8 -*-

from django import forms

from produtos.models.produto import Produto


class ProdutoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #must use the estabelecimento id in the init, to test the unique_together after on the clean methods
        self.estabelecimentoid = kwargs.pop('estabelecimentoid')

        super(ProdutoForm, self).__init__(*args, **kwargs)

    def clean(self):
        #validate is the name already exist and check if it's and edit
        #this is checking for the unique_together that does not work with exlucde fields, stupid django
        if (Produto.objects.filter(estabelecimento_id=self.estabelecimentoid, nome=self.cleaned_data['nome']).exists() and
            Produto.objects.get(estabelecimento_id=self.estabelecimentoid,
                              nome=self.cleaned_data['nome']).id != self.instance.id):

            raise forms.ValidationError("Já existe um Produto com o nome: " + self.cleaned_data['nome'])

        return self.cleaned_data


    class Meta:
        model = Produto
        fields = ['nome', 'descricao']