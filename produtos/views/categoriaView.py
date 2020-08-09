from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, UpdateView

from produtos.forms.categoriaForm import CategoriaForm
from produtos.models.categoria import Categoria


class CategoriaCreate(LoginRequiredMixin, FormView):

    form_class = CategoriaForm
    template_name = 'categoria.html'
    success_url = reverse_lazy('CATEGORIA')

    def form_valid(self, form):
        #add the estabelecimento na categoria antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(CategoriaCreate, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs

class CategoriaEdit(LoginRequiredMixin, UpdateView):

    form_class = CategoriaForm
    template_name = 'categoria.html'
    success_url = reverse_lazy('CATEGORIA')
    model = Categoria

    def get_form_kwargs(self):
        #necessary to validate unique_together on the form, dur django limitation
        kwargs = super(CategoriaEdit, self).get_form_kwargs()
        kwargs['estabelecimentoid'] = self.request.user.profile.estabelecimento.pk
        return kwargs


class CategoriaAtivar(LoginRequiredMixin, SingleObjectMixin, View):

    def get(self, request, *args, **kwargs):

        #caso alguém tente usar a URL diretamente para alterar o objeto
        messages.add_message(request, messages.INFO, 'Método não suportado.')
        return redirect("CATEGORIA")

    def post(self, request, *args, **kwargs):

        try:
            categoria = Categoria.objects.get(id=kwargs['pk'], estabelecimento=self.request.user.profile.estabelecimento)

            if categoria.ativo:
                categoria.ativo = False
            else:
                categoria.ativo = True
            categoria.save()

        except:
            messages.add_message(request, messages.INFO, 'Categoria não encontrada.')
        return redirect("CATEGORIA")


class CategoriaView(LoginRequiredMixin, generic.ListView):

    model = Categoria
    context_object_name = 'Categoria'
    template_name = 'categoria_list.html'

    def get_queryset(self):

        #carrega todas as categorias do estabelecimento
        queryset = Categoria.objects.filter(estabelecimento=self.request.user.profile.estabelecimento)
        return queryset