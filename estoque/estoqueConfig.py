from django.apps import AppConfig


class EstoqueConfig(AppConfig):
    name = 'estoque'
    label = 'estoque'

    def ready(self):

        import estoque.models.signals