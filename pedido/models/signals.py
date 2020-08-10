from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver

from pedido.models.pedido import Pedido

#keep the track of the order status, to not allow for example, set a order that is incomplete as delievred
from pedido.models.pedidoproduto import PedidoProduto
from produtos.models import Preco


@receiver(m2m_changed, sender=Pedido.produtos.through)
def updatepedidostatus(sender, instance, **kwargs):

    if kwargs['action'] == 'post_clear':

        #set to false the order complete status
        instance.pedidoprodutoscompleto = False
        instance.pedidocompleto = False
        instance.save()

    elif kwargs['action'] == 'post_add':

        #set to false the order complete status, but now the producst are in place
        instance.pedidoprodutoscompleto = True
        instance.pedidocompleto = False
        instance.save()

@receiver(pre_save, sender=Pedido)
def updatevalorpedido(sender, instance, **kwargs):
    #calcule the value of rhe order, based on all the data

    if instance.is_completo():

        valor_total = 0.0
        produtos = PedidoProduto.objects.get(pedido=instance)
        for produto in produtos:

            #get the latest price for the product
            preco = Preco.objects.get(produto=produto,
                                      canalvenda=instance.canalvenda,
                                      datafim=None,
                                      estabelecimento=instance.estabelecimento)

            valor_total = round(valor_total + (preco.preco * produto.quantidade),2)

        #after get the total value from the products, need to calculate the addition from the order itself
        #the order of the addtions is important. Start with: acrescima/desconto and then embalagem and entrega

        if instance.desconto != 0:

            valor_total = valor_total * round((1 + instance.desconto/100),2)

        elif instance.acrescimo != 0:

            valor_total = valor_total * round((1 + instance.acrescimo/100),2)

        valor_total = valor_total + instance.embalagem + instance.entrega

        instance.valor = valor_total


