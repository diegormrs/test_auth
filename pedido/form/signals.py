from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from pedido.models.pedido import Pedido

#keep the track of the order status, to not allow for example, set a order that is incomplete as delievred
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