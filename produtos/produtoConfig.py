from django.apps import AppConfig


class ProdutosConfig(AppConfig):
    name = 'produtos'
    label = 'produtos'

    def ready(self):
        import produtos.models.signals