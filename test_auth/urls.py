from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from estoque.views.estoque import CompraCreate, CompraView, EstoqueView, PerdaView, PerdaCreate
from pedido.views.clienteView import ClienteView, ClienteCreate, ClienteAtivar, ClienteEdit
from pedido.views.pedidoView import PedidoView, PedidoCreate, PedidoProdutoCreate, PedidoFinalizarCreate, PedidoDetalhe
from produtos.views.categoriaView import CategoriaCreate, CategoriaEdit, CategoriaAtivar, CategoriaView
from produtos.views.canalvendaView import CanalVendaCreate, CanalVendaView, CanalVendaAtivar, CanalVendaEdit
from produtos.views.custoView import CustoView, CustoCreate, CustoAtivar, CustoEdit
from produtos.views.materiaprimaView import MateriaPrimaCreate, MateriaPrimaEdit, MateriaPrimaAtivar, MateriaPrimaView
from produtos.views.produto import ProdutoCreate, ProdutoEdit, ProdutoAtivar, ProdutoView, ProdutoMateriaPrimaCreate, \
    ProdutoCanalCreate, ProdutoCustoCreate, ProdutoLucroCreate, ProdutoDetalhe
from produtos.views.sistemaView import SistemaView

urlpatterns = [

    path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('sistema/', SistemaView.as_view(), name="SISTEMA"),

    #####CATEGORIAS######
    path('categoria/criar/', CategoriaCreate.as_view(), name="CATEGORIA_CRIAR"),
    re_path('categoria/editar/(?P<pk>\d+)/$', CategoriaEdit.as_view(), name="CATEGORIA_EDITAR"),
    re_path('categoria/ativar/(?P<pk>\d+)/$', CategoriaAtivar.as_view(), name="CATEGORIA_ATIVAR"),
    path('categoria/', CategoriaView.as_view(), name="CATEGORIA"),

    #####CANAL VENDA######
    path('canalvenda/criar/', CanalVendaCreate.as_view(), name="CANALVENDA_CRIAR"),
    re_path('canalvenda/editar/(?P<pk>\d+)/$', CanalVendaEdit.as_view(), name="CANALVENDA_EDITAR"),
    re_path('canalvenda/ativar/(?P<pk>\d+)/$', CanalVendaAtivar.as_view(), name="CANALVENDA_ATIVAR"),
    path('canalvenda/', CanalVendaView.as_view(), name="CANALVENDA"),

    #####CUSTO######
    path('custo/criar/', CustoCreate.as_view(), name="CUSTO_CRIAR"),
    re_path('custo/editar/(?P<pk>\d+)/$', CustoEdit.as_view(), name="CUSTO_EDITAR"),
    re_path('custo/ativar/(?P<pk>\d+)/$', CustoAtivar.as_view(), name="CAUSTO_ATIVAR"),
    path('custo/', CustoView.as_view(), name="CUSTO"),

    #####MATERIA-PRIMA######
    path('materiaprima/criar/', MateriaPrimaCreate.as_view(), name="MATERIAPRIMA_CRIAR"),
    re_path('materiaprima/editar/(?P<pk>\d+)/$', MateriaPrimaEdit.as_view(), name="MATERIAPRIMA_EDITAR"),
    re_path('materiaprima/ativar/(?P<pk>\d+)/$', MateriaPrimaAtivar.as_view(), name="MATERIAPRIMA_ATIVAR"),
    path('materiaprima/', MateriaPrimaView.as_view(), name="MATERIAPRIMA"),

    #####PRODUTO######
    path('produto/criar/', ProdutoCreate.as_view(), name="PRODUTO_CRIAR"),
    re_path('produto/criar/materia/(?P<pk>\d+)/$', ProdutoMateriaPrimaCreate.as_view(), name="PRODUTO_MATERIAPRIMA_CRIAR"),
    re_path('produto/criar/canal/(?P<pk>\d+)/$', ProdutoCanalCreate.as_view(), name="PRODUTO_CANAL_CRIAR"),
    re_path('produto/criar/custo/(?P<pk>\d+)/$', ProdutoCustoCreate.as_view(), name="PRODUTO_CUSTO_CRIAR"),
    re_path('produto/criar/lucro/(?P<pk>\d+)/$', ProdutoLucroCreate.as_view(), name="PRODUTO_LUCRO_CRIAR"),
    re_path('produto/editar/(?P<pk>\d+)/$', ProdutoEdit.as_view(), name="PRODUTO_EDITAR"),
    re_path('produto/ativar/(?P<pk>\d+)/$', ProdutoAtivar.as_view(), name="PRODUTO_ATIVAR"),
    re_path('produto/detalhe/(?P<pk>\d+)/$', ProdutoDetalhe.as_view(), name="PRODUTO_DETALHE"),
    path('produto/', ProdutoView.as_view(), name="PRODUTO"),

    #####COMPRA######
    path('compra/criar/', CompraCreate.as_view(), name="COMPRA_CRIAR"),
    path('perda/criar/', PerdaCreate.as_view(), name="PERDA_CRIAR"),
    path('compra/', CompraView.as_view(), name="COMPRA"),
    path('perda/', PerdaView.as_view(), name="PERDA"),
    path('estoque/', EstoqueView.as_view(), name="ESTOQUE"),

    #####CLIENTES######
    path('cliente/criar/', ClienteCreate.as_view(), name="CLIENTE_CRIAR"),
    re_path('cliente/editar/(?P<pk>\d+)/$', ClienteEdit.as_view(), name="CLIENTE_EDITAR"),
    re_path('cliente/ativar/(?P<pk>\d+)/$', ClienteAtivar.as_view(), name="CLIENTE_ATIVAR"),
    path('cliente/', ClienteView.as_view(), name="CLIENTE"),

    #####PRODUTO######
    path('pedido/criar/', PedidoCreate.as_view(), name="PEDIDO_CRIAR"),
    re_path('pedido/criar/produto/(?P<pk>\d+)/$', PedidoProdutoCreate.as_view(), name="PEDIDO_CRIAR_PRODUTO"),
    re_path('pedido/criar/finalizar/(?P<pk>\d+)/$', PedidoFinalizarCreate.as_view(), name="PEDIDO_CRIAR_FINALIZAR"),
    re_path('pedido/detalhe/(?P<pk>\d+)/$', PedidoDetalhe.as_view(), name="PEDIDO_DETALHE"),
    path('pedido/', PedidoView.as_view(), name="PEDIDO"),


    #URLs from the allayth app
    path('accounts/', include('allauth.urls')),
]
