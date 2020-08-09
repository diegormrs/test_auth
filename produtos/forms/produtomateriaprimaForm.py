# -*- coding: UTF-8 -*-

from django import forms

from produtos.models.materiaprima import MateriaPrima
from produtos.models.produto import Produto
from produtos.models.produtomateria import ProdutoMateriaPrima


# precisa usar modelform para ter um instancia do model para inserir o estabeleciemnto no view
class ProdutoMateriaPrimaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.estabelecimentoid = kwargs.pop('estabelecimentoid')
        self.produtoid = kwargs.pop('produtoid')

        super(ProdutoMateriaPrimaForm, self).__init__(*args, **kwargs)

        # pega as materias primas ordenando por categoria para exibicao na tela

        fields = MateriaPrima.objects.filter(estabelecimento=self.estabelecimentoid).order_by('categoria')
        self.instance = Produto.objects.get(id=self.produtoid)

        #cria um campo para cada materia existente no sistems para aquele estabelecimento
        #num achei outro jeito de entrar a quantidade de matéria por produto usando os fields standart
        for materia in fields:
            self.fields[materia.nome.replace(" ", "") +"_"+str(materia.id)] = forms.CharField(
                label=materia.nome,
                required=False,
                localize=True,
                widget=forms.NumberInput({
                    'categoria': materia.categoria.id,
                    'categorianome': materia.categoria.nome,
                }))

            try:
                #get the materia related to the product to fulfill the initial quantity when editing the materia/produto relation
                materiasproduto = ProdutoMateriaPrima.objects.get(produto_id=self.produtoid, materiaprima=materia)
                self.fields[materia.nome.replace(" ", "") +"_"+str(materia.id)].initial = "{:.2f}".format(materiasproduto.quantidade)

            except Exception as e:
                pass

############################################################################################################
############################################################################################################

    def clean(self):

        #precisa copiar para num alterar os dois durante a validacao, caso contrario error irao aparecer no for
        cleaned_data = self.cleaned_data.copy()
        has_value = False

        for key, data in self.cleaned_data.items():
        #checa se o campo é númerico e se ao menos uma foi preenchido
            try:
                if data:
                    float(data)
                    has_value = True
                else:
                    #se não tiver dados remove a entrada do dict
                    #isso ajuda na hora de salvar para evitar save desnecessários
                    del cleaned_data[key]
            except:
                raise forms.ValidationError("A quantidade de matéria no produto precisa ser um número válido.")

        if not has_value:
            raise forms.ValidationError("Ao menos uma matéria precisa ter sua quantidade informada")

        return cleaned_data

############################################################################################################
############################################################################################################

    def save(self, commit=True):

        # deleta todos os antigas materias-primas relacionadas com o produto antes de salvar as novas
        produtomateriaprima = ProdutoMateriaPrima.objects.filter(produto_id=self.produtoid)
        produtomateriaprima.delete()

        for key, data in self.cleaned_data.items():

            materia = MateriaPrima.objects.get(id=key.rsplit('_', 1)[-1])
            produtomateriaprima = ProdutoMateriaPrima(produto_id=self.produtoid,
                                                      materiaprima=materia,
                                                      quantidade=float(data))

            produtomateriaprima.save()

############################################################################################################
############################################################################################################

    # remove todos os campos, pois o form é criado dinamicamente pedendendo das materias salvas no sistema
    class Meta:
        model = Produto
        fields = []