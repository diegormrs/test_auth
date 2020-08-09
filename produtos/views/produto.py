from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormView, UpdateView
from produtos.forms.produto import ProdutoForm
from produtos.forms.produtocanalForm import ProdutoCanalForm
from produtos.forms.produtocustoForm import ProdutoCustoForm
from produtos.forms.produtolucroForm import ProdutoLucroForm
from produtos.forms.produtomateriaprimaForm import ProdutoMateriaPrimaForm
from produtos.models.produto import Produto


class ProdutoCreate(LoginRequiredMixin, FormView):

    form_class = ProdutoForm
    template_name = 'produto.html'
    success_url = reverse_lazy('PRODUTO_MATERIAPRIMA_CRIAR')

    def form_valid(self, form):
        #add the estabelecimento na matéria-prima antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        #passa o id do produto para próxiam tela
        return HttpResponseRedirect(self.get_success_url(produtoid=form.instance.id))

    def get_success_url(self, **kwargs):
        #get the product id to keep ideiting the same one
        return reverse_lazy('PRODUTO_MATERIAPRIMA_CRIAR', kwargs={'pk': kwargs.pop('produtoid')})

    def get_form_kwargs(self):

        kwargs = super(ProdutoCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs

############################################################################################################
############################################################################################################

class ProdutoMateriaPrimaCreate(LoginRequiredMixin, FormView):

    form_class = ProdutoMateriaPrimaForm
    template_name = 'produto.html'

    def get_form_kwargs(self):

        kwargs = super(ProdutoMateriaPrimaCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        kwargs['produtoid'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        #add the estabelecimento na matéria-prima antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        #pega o Id fo produto para continuar a edicao do mesmo id
        return reverse_lazy('PRODUTO_CUSTO_CRIAR', kwargs={'pk': self.kwargs.pop('pk')})

############################################################################################################
############################################################################################################

class ProdutoCustoCreate(LoginRequiredMixin, FormView):

    form_class = ProdutoCustoForm
    template_name = 'produto.html'

    def get_form_kwargs(self):

        kwargs = super(ProdutoCustoCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        kwargs['produtoid'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        #add the estabelecimento na matéria-prima antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        #pega o Id fo produto para continuar a edicao do mesmo id
        return reverse_lazy('PRODUTO_CANAL_CRIAR', kwargs={'pk': self.kwargs.pop('pk')})

############################################################################################################
############################################################################################################
class ProdutoCanalCreate(LoginRequiredMixin, FormView):

    form_class = ProdutoCanalForm
    template_name = 'produto.html'

    def get_form_kwargs(self):

        kwargs = super(ProdutoCanalCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        kwargs['produtoid'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        #add the estabelecimento na matéria-prima antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save(commit=True)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        #pega o Id fo produto para continuar a edicao do mesmo id
        return reverse_lazy('PRODUTO_LUCRO_CRIAR', kwargs={'pk': self.kwargs.pop('pk')})

############################################################################################################
############################################################################################################

class ProdutoLucroCreate(LoginRequiredMixin, UpdateView):

    form_class = ProdutoLucroForm
    template_name = 'produto.html'
    success_url = reverse_lazy('PRODUTO')
    model = Produto

    def get_form_kwargs(self):

        kwargs = super(ProdutoLucroCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        kwargs['produtoid'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        #add the estabelecimento na matéria-prima antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        return HttpResponseRedirect(self.get_success_url())

############################################################################################################
############################################################################################################

class ProdutoEdit(LoginRequiredMixin, UpdateView):

    form_class = ProdutoForm
    template_name = 'produto.html'
    model = Produto

    def get_success_url(self, **kwargs):

        #pega o Id fo produto para continuar a edicao do mesmo id
        return reverse_lazy('PRODUTO_MATERIAPRIMA_CRIAR', kwargs={'pk': self.kwargs.pop('pk')})

    def get_form_kwargs(self):

        kwargs = super(ProdutoEdit, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs
############################################################################################################
############################################################################################################

class ProdutoAtivar(LoginRequiredMixin, SingleObjectMixin, View):

    def get(self, request, *args, **kwargs):

        #caso alguém tente usar a URL diretamente para alterar o objeto
        messages.add_message(request, messages.INFO, 'Método não suportado.')
        return redirect("PRODUTO")

    def post(self, request, *args, **kwargs):

        try:
            produto = Produto.objects.get(id=kwargs['pk'], estabelecimento=self.request.user.profile.estabelecimento)

            if produto.ativo:
                produto.ativo = False
            else:
                produto.ativo = True
            produto.save()

        except:
            messages.add_message(request, messages.INFO, 'Produto não encontrada.')
        return redirect("PRODUTO")

############################################################################################################
############################################################################################################

class ProdutoView(LoginRequiredMixin, generic.ListView):

    model = Produto
    context_object_name = 'Produto'
    template_name = 'produto_list.html'

    def get_queryset(self):

        #carrega todas as materia-rimas do estabelecimento
        queryset = Produto.objects.filter(estabelecimento=self.request.user.profile.estabelecimento)
        return queryset

############################################################################################################
############################################################################################################

class ProdutoDetalhe(LoginRequiredMixin, DetailView):

    model = Produto
    context_object_name = 'Produto'
    template_name = 'produto_detalhe.html'

    def get_object(self, queryset=None):

        #carrega todas as materia-rimas do estabelecimento
        object = Produto.objects.get(estabelecimento=self.request.user.profile.estabelecimento,
                                          id=self.kwargs['pk'])
        return object
