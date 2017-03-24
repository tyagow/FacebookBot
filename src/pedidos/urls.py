from django.conf.urls import url

from src.pedidos.views import PedidoListView, PedidoDetailView, PedidoUpdateView

urlpatterns = [
    url(r'^$', PedidoListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PedidoDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', PedidoUpdateView.as_view(), name='update'),
]
