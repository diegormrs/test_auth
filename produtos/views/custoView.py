from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, UpdateView

from produtos.forms.custoForm import CustoForm
from produtos.models.custo import Custo


class CustoCreate(LoginRequiredMixin, FormView):

    form_class = CustoForm
    template_name = 'custo.html'
    success_url = reverse_lazy('CUSTO')

    def form_valid(self, form):
        #add the estabelecimento na categoria antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(CustoCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs

class CustoEdit(LoginRequiredMixin, UpdateView):

    form_class = CustoForm
    template_name = 'custo.html'
    success_url = reverse_lazy('CUSTO')
    model = Custo

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(CustoEdit, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs

class CustoAtivar(LoginRequiredMixin, SingleObjectMixin, View):

    def get(self, request, *args, **kwargs):

        #caso alguém tente usar a URL diretamente para alterar o objeto
        messages.add_message(request, messages.INFO, 'Método não suportado.')
        return redirect("CUSTO")

    def post(self, request, *args, **kwargs):

        try:
            custo = Custo.objects.get(id=kwargs['pk'], estabelecimento=self.request.user.profile.estabelecimento)

            if custo.ativo:
                custo.ativo = False
            else:
                custo.ativo = True
            custo.save()

        except:
            messages.add_message(request, messages.INFO, 'Custo não encontrado.')
        return redirect("CUSTO")

class CustoView(LoginRequiredMixin, generic.ListView):

    model = Custo
    context_object_name = 'Custo'
    template_name = 'custo_list.html'

    def get_queryset(self):

        #carrega todas as categorias do estabelecimento
        queryset = Custo.objects.filter(estabelecimento=self.request.user.profile.estabelecimento)
        return queryset