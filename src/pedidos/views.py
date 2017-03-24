from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from src.pedidos.forms import PedidoForm
from src.pedidos.models import Pedido


class PedidoListView(ListView):
    model = Pedido

    def get_queryset(self):
        return Pedido.objects.hoje()
        # return Pedido.objects.by_user(self.request.user)


class PedidoDetailView(DetailView):
    model = Pedido


class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
