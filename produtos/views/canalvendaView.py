from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, UpdateView

from produtos.forms.canavendaForm import CanalVendaForm
from produtos.models.canalvenda import CanalVenda


class CanalVendaCreate(LoginRequiredMixin, FormView):

    form_class = CanalVendaForm
    template_name = 'canalvenda.html'
    success_url = reverse_lazy('CANALVENDA')

    def form_valid(self, form):
        #add the estabelecimento na categoria antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(CanalVendaCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs

class CanalVendaEdit(LoginRequiredMixin, UpdateView):

    form_class = CanalVendaForm
    template_name = 'canalvenda.html'
    success_url = reverse_lazy('CANALVENDA')
    model = CanalVenda

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(CanalVendaEdit, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs

class CanalVendaAtivar(LoginRequiredMixin, SingleObjectMixin, View):

    def get(self, request, *args, **kwargs):

        #caso alguém tente usar a URL diretamente para alterar o objeto
        messages.add_message(request, messages.INFO, 'Método não suportado.')
        return redirect("CANALVENDA")

    def post(self, request, *args, **kwargs):

        try:
            canalvenda = CanalVenda.objects.get(id=kwargs['pk'], estabelecimento=self.request.user.profile.estabelecimento)

            if canalvenda.ativo:
                canalvenda.ativo = False
            else:
                canalvenda.ativo = True
            canalvenda.save()

        except:
            messages.add_message(request, messages.INFO, 'Canale de Venda não encontrado.')
        return redirect("CANALVENDA")

class CanalVendaView(LoginRequiredMixin, generic.ListView):

    model = CanalVenda
    context_object_name = 'Canal de Venda'
    template_name = 'canalvenda_list.html'

    def get_queryset(self):

        #carrega todas as categorias do estabelecimento
        queryset = CanalVenda.objects.filter(estabelecimento=self.request.user.profile.estabelecimento)
        return queryset