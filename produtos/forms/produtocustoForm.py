# -*- coding: UTF-8 -*-

from django import forms

from produtos.models.custo import Custo
from produtos.models.produto import Produto


# precisa usar modelform para ter um instancia do model para inserir o estabeleciemnto no view
class ProdutoCustoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.estabelecimentoid = kwargs.pop('estabelecimentoid')
        self.produtoid = kwargs.pop('produtoid')

        super(ProdutoCustoForm, self).__init__(*args, **kwargs)

############################################################################################################
        #pega todos os canais de venda possivei e checa se ees já estão marcados no pedido

        self.fields['custos'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=True,
                                                               queryset=Custo.objects.filter(ativo=True,
                                                               estabelecimento_id= self.estabelecimentoid),
                                                               #if there is data wull bring the values from table to the form
                                                               initial=[c.id for c in Produto.objects.get(id=self.produtoid).custos.all()])

############################################################################################################
############################################################################################################

    def save(self, commit=True):

        produto = Produto.objects.get(id=self.produtoid)
        produto.custos.clear()
        #add all the custos on the table at once
        produto.custos.add(*self.cleaned_data['custos'])

    class Meta:
        model = Produto
        fields = ['custos']