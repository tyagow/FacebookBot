from django.conf.urls import url

from src.pedidos.views import PedidoListView

urlpatterns = [
    url(r'^$', PedidoListView.as_view(), name='list'),
]
