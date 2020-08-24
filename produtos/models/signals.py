from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from django.utils.timezone import now

from estoque.models.estoque import Estoque
from produtos.models import Preco
from produtos.models.produto import Produto
from produtos.models.produtomateria import ProdutoMateriaPrima


@receiver(post_save, sender=Produto.materias.through)
def updateprodutomaterias(sender, instance, **kwargs):
    #set materiacompleto to true
    instance.produto.materiacompleto = True
    instance.produto.canalcompleto = False
    instance.produto.custocompleto = False
    instance.produto.precocompleto = False
    instance.produto.updatepreco = True

    instance.produto.save()

@receiver(m2m_changed, sender=Produto.custos.through)
def updateprodutocustos(sender, instance, **kwargs):

    if kwargs['action'] == 'post_clear':

        #seta para false o custocompleto, pois no meio tempo ele esta de fato inválido
        instance.materiacompleto = True
        instance.custocompleto = False
        instance.canalcompleto = False
        instance.precocompleto = False
        instance.save()

    elif kwargs['action'] == 'post_add':

        instance.materiacompleto = True
        instance.custocompleto = True
        instance.canalcompleto = False
        instance.precocompleto = False
        instance.save()

@receiver(m2m_changed, sender=Produto.canais.through)
def updateprodutocanais(sender, instance, **kwargs):

    if kwargs['action'] == 'post_clear':

        #seta canaois completo to false apos limpar as antigas entradas
        instance.materiacompleto = True
        instance.canalcompleto = False
        instance.custocompleto = True
        instance.precocompleto = False
        instance.save()

    elif kwargs['action'] == 'post_add':

        instance.materiacompleto = True
        instance.canalcompleto = True
        instance.custocompleto = True
        instance.precocompleto = False
        instance.save()

@receiver(pre_save, sender=Produto)
def updateprodutopreco(sender, instance, **kwargs):
    #salva o antigo preco antes de mudar o produto para o novo valor

    if instance.is_completo() and instance.updatepreco:

        precos = Preco.objects.filter(produto=instance,
                                      datafim=None)
        if precos:
            for preco in precos:
                #set the final date on the price to not be active anymore
                preco.datafim = now()
                preco.save()

        #get all the materias from the prodcut to calculate the base value
        materias = ProdutoMateriaPrima.objects.filter(produto_id=instance.id)
        precobase = 0

        for materia in materias:
            #find materia price
            estoque = Estoque.objects.get(materia=materia.materiaprima)
            precobase = precobase + round(materia.quantidade * estoque.valorunitario, 2)

        custos = instance.custos.all()

        porcentagemtotal = 0
        custototal = 0

        #sum all the custos before add to the price of the materias
        for custo in custos:

            if custo.tipo == 'porcentagem':
                porcentagemtotal = porcentagemtotal + custo.valor
            else:
                custototal = custototal + custo.valor

        #first add the custo in money
        precobase = precobase + custototal

        #them add the custos in percentage
        if porcentagemtotal > 0:
            precobase = round(precobase * (1 + porcentagemtotal/100), 2)
        instance.precobase = precobase

        canaisvenda = instance.canais.all()
        #save one price for each cnanal de venda where the product is sell
        for canal in canaisvenda:
            #create the prie with a lucro and also based on the chanell value added
            precocanal = Preco(preco = round(instance.precolucro() * (1 + canal.porcentagem/100), 2),
                               produto = instance,
                               canalvenda = canal,
                               estabelecimento= instance.estabelecimento)
            precocanal.save()

        #set to false, if not it will try to updte the price when the name is edited
        instance.updatepreco = False

    elif instance.materiacompleto and instance.canalcompleto and instance.custocompleto and instance.updatepreco:

        instance.precocompleto = True