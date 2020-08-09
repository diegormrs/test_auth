from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, UpdateView

from produtos.forms.materiaprimaForm import MateriaPrimaForm
from produtos.models.categoria import Categoria
from produtos.models.materiaprima import MateriaPrima


class MateriaPrimaCreate(LoginRequiredMixin, FormView):

    form_class = MateriaPrimaForm
    template_name = 'materiaprima.html'
    success_url = reverse_lazy('MATERIAPRIMA')

    def form_valid(self, form):
        #add the estabelecimento na matéria-prima antes de salvar
        form.instance.estabelecimento = self.request.user.profile.estabelecimento
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class MateriaPrimaEdit(LoginRequiredMixin, UpdateView):

    form_class = MateriaPrimaForm
    template_name = 'materiaprima.html'
    success_url = reverse_lazy('MATERIAPRIMA')
    model = MateriaPrima


class MateriaPrimaAtivar(LoginRequiredMixin, SingleObjectMixin, View):

    def get(self, request, *args, **kwargs):

        #caso alguém tente usar a URL diretamente para alterar o objeto
        messages.add_message(request, messages.INFO, 'Método não suportado.')
        return redirect("MATERIAPRIMA")

    def post(self, request, *args, **kwargs):

        try:
            materiaprima = MateriaPrima.objects.get(id=kwargs['pk'], estabelecimento=self.request.user.profile.estabelecimento)

            if materiaprima.ativo:
                materiaprima.ativo = False
            else:
                materiaprima.ativo = True
            materiaprima.save()

        except:
            messages.add_message(request, messages.INFO, 'Matéria-Prima não encontrada.')
        return redirect("MATERIAPRIMA")


class MateriaPrimaView(LoginRequiredMixin, generic.ListView):

    model = Categoria
    context_object_name = 'Matéria-Prima'
    template_name = 'materiaprima_list.html'

    def get_queryset(self):

        #carrega todas as materia-rimas do estabelecimento
        queryset = MateriaPrima.objects.filter(estabelecimento=self.request.user.profile.estabelecimento)
        return queryset