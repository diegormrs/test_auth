from django.apps import AppConfig


class PedidoConfig(AppConfig):
    name = 'pedido'
    label = 'pedido'

    def ready(self):
        import pedido.models
