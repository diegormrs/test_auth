# -*- coding: UTF-8 -*-

from django import forms

from pedido.models.pedido import Pedido
from pedido.models.pedidoproduto import PedidoProduto
from produtos.models.produto import Produto

class PedidoProdutoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.estabelecimentoid = kwargs.pop('estabelecimentoid')
        self.pedidoid = kwargs.pop('pedidoid')

        super(PedidoProdutoForm, self).__init__(*args, **kwargs)

        #get all the products avaible to be used in the order
        #Only active and complete products

        fields = Produto.objects.filter(estabelecimento=self.estabelecimentoid,
                                        ativo=True,
                                        materiacompleto = True,
                                        canalcompleto = True,
                                        custocompleto = True,
                                        precocompleto = True)

        #create a field for each product, so the amount can be entered
        #also, uses the id at the end, to be used as refrence on the save method
        for produto in fields:
            self.fields[produto.nome.replace(" ", "") +"_"+str(produto.id)] = forms.CharField(
                label=produto.nome,
                required=False,
                localize=True,
                widget=forms.NumberInput({}))

            try:#need to implemnte something to edit pages
                pass

            except Exception as e:
                pass

############################################################################################################
############################################################################################################
    def clean(self):

        # need to copy the data to no cause problems
        cleaned_data = self.cleaned_data.copy()
        has_value = False

        for key, data in self.cleaned_data.items():
            # checa se o campo é númerico e se ao menos uma foi preenchido
            try:
                if data:
                    float(data)
                    has_value = True
                else:
                    # if there is no data in the fields, just remove it
                    # this avoid desnecessary saves on the DB
                    del cleaned_data[key]
            except:
                raise forms.ValidationError("A quantidade de Produtos no Pedido precisa ser um número válido.")

        if not has_value:
            raise forms.ValidationError("Ao menos um Produto precisa ter sua quantidade informada")

        return cleaned_data

############################################################################################################
############################################################################################################
    def save(self, commit=True):

        # delete all the old entries related to producsts in the order
        produtospedido = PedidoProduto.objects.filter(produto_id=self.pedidoid)
        produtospedido.delete()

        for key, data in self.cleaned_data.items():
            #use the trick to get the id from the name of the field
            produto = Produto.objects.get(id=key.rsplit('_', 1)[-1])
            produtopedido = PedidoProduto(pedido_id=self.pedidoid,
                                                produto=produto,
                                                quantidade=float(data))

            produtopedido.save()
        pedido = Pedido.objects.get(id=self.pedidoid)
        #set produtos from pedido to complete
        pedido.pedidoprodutoscompleto = True
        pedido.save()

    class Meta:
        model = Pedido
        fields = []