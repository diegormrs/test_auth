# -*- coding: UTF-8 -*-

from django import forms

from produtos.models.canalvenda import CanalVenda
from produtos.models.produto import Produto


# precisa usar modelform para ter um instancia do model para inserir o estabeleciemnto no view
class ProdutoCanalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.estabelecimentoid = kwargs.pop('estabelecimentoid')
        self.produtoid = kwargs.pop('produtoid')

        super(ProdutoCanalForm, self).__init__(*args, **kwargs)

############################################################################################################
        #pega todos os canais de venda possivei e checa se ees já estão marcados no pedido

        self.fields['canais'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=True,
                                                               queryset=CanalVenda.objects.filter(ativo=True,
                                                               estabelecimento_id= self.estabelecimentoid),
                                                               initial=[c.id for c in Produto.objects.get(id=self.produtoid).canais.all()])

############################################################################################################
############################################################################################################
    def save(self, commit=True):

        produto = Produto.objects.get(id=self.produtoid)
        produto.canais.clear()
        produto.canais.add(*self.cleaned_data['canais'])

    # remove todos os campos, pois o form é criado dinamicamente pedendendo das materias salvas no sistema
    class Meta:
        model = Produto
        fields = ['canais']