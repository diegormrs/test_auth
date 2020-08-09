from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, UpdateView

from pedido.form.clienteForm import ClienteForm
from pedido.models.cliente import Cliente
from produtos.models.canalvenda import CanalVenda


class ClienteCreate(LoginRequiredMixin, FormView):

    form_class = ClienteForm
    template_name = 'cliente.html'
    success_url = reverse_lazy('CLIENTE')

    def form_valid(self, form):
        #add the estabelecimento na categoria antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(ClienteCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs

class ClienteEdit(LoginRequiredMixin, UpdateView):

    form_class = ClienteForm
    template_name = 'cliente.html'
    success_url = reverse_lazy('CLIENTE')
    model = Cliente

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(ClienteEdit, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs

class ClienteAtivar(LoginRequiredMixin, SingleObjectMixin, View):

    def get(self, request, *args, **kwargs):

        #in case someone try to use the URL directly to change the object
        messages.add_message(request, messages.INFO, 'Método não suportado.')
        return redirect("CLIENTE")

    def post(self, request, *args, **kwargs):

        try:
            cliente = Cliente.objects.get(id=kwargs['pk'], estabelecimento=self.request.user.profile.estabelecimento)

            if cliente.ativo:
                cliente.ativo = False
            else:
                cliente.ativo = True
            cliente.save()

        except:
            messages.add_message(request, messages.INFO, 'Cliente não encontrado.')
        return redirect("CLIENTE")

class ClienteView(LoginRequiredMixin, generic.ListView):

    model = CanalVenda
    context_object_name = 'Cliente'
    template_name = 'cliente_list.html'

    def get_queryset(self):

        #carrega todas as categorias do estabelecimento
        queryset = Cliente.objects.filter(estabelecimento=self.request.user.profile.estabelecimento)
        return queryset