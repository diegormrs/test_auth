from django.db.models.signals import pre_save, post_save, m2m_changed, pre_delete
from django.dispatch import receiver

from estoque.models.compra import Compra
from estoque.models.estoque import Estoque
from estoque.models.estoquehistorico import EstoqueHistorico
from estoque.models.perda import Perda
from produtos.models.produto import Produto



@receiver(post_save, sender=Compra)
def updatecompra(sender, instance, **kwargs):
    #needs to update the estoque quando uma compra é feita
    try:
        estoque = Estoque.objects.get(materia=instance.materia)

        #create historici with the preivous data
        estoquehistorico = EstoqueHistorico(materia=instance.materia,
                                            quantidadeantes=estoque.quantidade,
                                            valorantes=estoque.valor,
                                            valorunitarioantes=estoque.valorunitario,
                                            compra=instance,
                                            estabelecimento=instance.estabelecimento)

        estoque.quantidade = estoque.quantidade + instance.quantidade
        estoque.valor = estoque.valor + instance.valor
        estoque.valorunitario = round(estoque.valor / estoque.quantidade, 2)

        #add the data after the change on the stock and save as the new data
        estoquehistorico.quantidadedepois = estoque.quantidade
        estoquehistorico.valordepois = estoque.valor
        estoquehistorico.valorunitariodepois = estoque.valorunitario
        estoquehistorico.save()

        estoque.save()
    #in case there is no stock yet, create one for the pleasure of god
    except:

        #if it's the first entry on the estoque, create it if the values from the compra
        estoque = Estoque(materia=instance.materia, quantidade=instance.quantidade, estabelecimento=instance.estabelecimento,
                              valorunitario=instance.precounitario, valor=instance.valor)
        #create the initial data on the historic
        estoquehistorico = EstoqueHistorico(materia=instance.materia,
                                            quantidadeantes=0,
                                            valorantes=0,
                                            valorunitarioantes=0,
                                            quantidadedepois=instance.quantidade,
                                            valordepois=instance.valor,
                                            valorunitariodepois=instance.precounitario,
                                            compra=instance,
                                            estabelecimento=instance.estabelecimento)
        estoquehistorico.save()
        estoque.save()

############################################################################################################
############################################################################################################

@receiver(post_save, sender=Perda)
def updateperda(sender, instance, **kwargs):

    #needs to update the estoque quando uma perda é
    estoque = Estoque.objects.get(materia=instance.materia)

    #create the preivous data before the upate the values on the main stock
    estoquehistorico = EstoqueHistorico(materia=instance.materia,
                                        quantidadeantes=estoque.quantidade,
                                        valorantes=estoque.valor,
                                        valorunitarioantes=estoque.valorunitario,
                                        perda=instance,
                                        estabelecimento=instance.estabelecimento)

    estoque.quantidade = estoque.quantidade - instance.quantidade
    #of there s notghin in the stock, there value is zero
    if estoque.quantidade > 0:
        estoque.valorunitario = round(estoque.valor / estoque.quantidade, 2)
    else:
        estoque.valorunitario = 0

    # add the data after the change on the stock and save as the new data
    estoquehistorico.quantidadedepois = estoque.quantidade
    estoquehistorico.valordepois = estoque.valor
    estoquehistorico.valorunitariodepois = estoque.valorunitario
    estoquehistorico.save()

    estoque.save()
