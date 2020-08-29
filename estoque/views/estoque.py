from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from estoque.form.compraForm import CompraForm
from estoque.form.perdaForm import PerdaForm
from estoque.models.compra import Compra
from django.http import HttpResponseRedirect
from django.views import generic, View

from estoque.models.estoque import Estoque
from estoque.models.estoquehistorico import EstoqueHistorico
from estoque.models.perda import Perda

class CompraCreate(LoginRequiredMixin, FormView):

    form_class = CompraForm
    template_name = 'compra.html'
    success_url = reverse_lazy('COMPRA')

    def form_valid(self, form):
        #add the estabelecimento na categoria antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        #set the user hat made the buy, this is important for audit
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(CompraCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs

############################################################################################################
############################################################################################################

class PerdaCreate(LoginRequiredMixin, FormView):

    form_class = PerdaForm
    template_name = 'perda.html'
    success_url = reverse_lazy('PERDA')

    def form_valid(self, form):
        #add the estabelecimento na categoria antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        #set the user hat made the buy, this is important for audit
        form.instance.user = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(PerdaCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs

############################################################################################################
############################################################################################################

class CompraView(LoginRequiredMixin, generic.ListView):

    model = Compra
    context_object_name = 'Compra'
    template_name = 'compra_list.html'

    def get_queryset(self):

        #carrega todas as materia-rimas do estabelecimento
        queryset = Compra.objects.filter(estabelecimento=self.request.user.profile.estabelecimento)
        return queryset

############################################################################################################
############################################################################################################

class EstoqueView(LoginRequiredMixin, generic.ListView):

    model = Estoque
    context_object_name = 'Estoque'
    template_name = 'estoque_list.html'

    def get_queryset(self):

        #carrega todas as materia-rimas do estabelecimento
        queryset = Estoque.objects.filter(estabelecimento=self.request.user.profile.estabelecimento)
        return queryset

############################################################################################################
############################################################################################################

class PerdaView(LoginRequiredMixin, generic.ListView):

    model = Perda
    context_object_name = 'Perda'
    template_name = 'perda_list.html'

    def get_queryset(self):

        #carrega todas as materia-rimas do estabelecimento
        queryset = Perda.objects.filter(estabelecimento=self.request.user.profile.estabelecimento)
        return queryset

############################################################################################################
############################################################################################################

class EstoqueHistoricoView(LoginRequiredMixin, generic.ListView):

    model = EstoqueHistorico
    context_object_name = 'Estoque Histórico'
    template_name = 'estoque_historico_list.html'

    def get_queryset(self):

        #carrega todas as materia-rimas do estabelecimento
        queryset = EstoqueHistorico.objects.filter(estabelecimento=self.request.user.profile.estabelecimento,
                                                   materia=self.kwargs['pk'])
        return queryset