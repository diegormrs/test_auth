from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView
from pedido.form.pedidoclienteForm import PedidoClienteForm
from pedido.form.pedidofinalizarForm import PedidoFinalizarForm
from pedido.form.pedidoprodutoForm import PedidoProdutoForm
from pedido.models.pedido import Pedido

class PedidoCreate(LoginRequiredMixin, FormView):

    form_class = PedidoClienteForm
    template_name = 'pedido.html'
    success_url = reverse_lazy('PEDIDO_CRIAR_PRODUTO')

    def form_valid(self, form):
        #add the estabelecimento na categoria antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        #need to pass the created pedido id to complete it
        return HttpResponseRedirect(self.get_success_url(pedidoid=form.instance.id))

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(PedidoCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        #must pass the user to the form, since the pedido object requires a user to be set
        kwargs['userid'] = self.request.user.id
        return kwargs

    def get_success_url(self, **kwargs):

        #pega o Id fo produto para continuar a edicao do mesmo id
        return reverse_lazy('PEDIDO_CRIAR_PRODUTO', kwargs={'pk': kwargs.pop('pedidoid')})

class PedidoProdutoCreate(LoginRequiredMixin, FormView):

    form_class = PedidoProdutoForm
    template_name = 'pedido.html'

    def form_valid(self, form):
        #add the estabelecimento na categoria antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        return HttpResponseRedirect(self.get_success_url(pedidoid=self.kwargs['pk']))

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(PedidoProdutoCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        kwargs['pedidoid'] = self.kwargs['pk']
        return kwargs

    def get_success_url(self, **kwargs):

        #get order id to keep in the same
        return reverse_lazy('PEDIDO_CRIAR_FINALIZAR', kwargs={'pk': kwargs.pop('pedidoid')})

class PedidoFinalizarCreate(LoginRequiredMixin, FormView):

    form_class = PedidoFinalizarForm
    template_name = 'pedido.html'
    success_url = reverse_lazy('PEDIDO')

    def form_valid(self, form):
        #add estabelecimento before saving it
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(PedidoFinalizarCreate, self).get_form_kwargs()
        #kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        ##kwargs['pedidoid'] = self.kwargs['pk']
        return kwargs

class PedidoView(LoginRequiredMixin, generic.ListView):

    model = Pedido
    context_object_name = 'Pedido'
    template_name = 'pedido_list.html'

    def get_queryset(self):

        #get all the pedidos from the last 30 days
        queryset = Pedido.objects.filter(estabelecimento=self.request.user.profile.estabelecimento)
        return queryset