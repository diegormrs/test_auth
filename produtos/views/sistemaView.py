from django.shortcuts import render
from django.views import View


class SistemaView(View):
    template_name = 'sidebar.html'

    def get(self, request):
        return render(request, self.template_name)
