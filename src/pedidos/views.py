from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from src.pedidos.models import Pedido


class PedidoListView(ListView):
    model = Pedido

    def get_queryset(self):
        return Pedido.objects.all()
        # return Pedido.objects.by_user(self.request.user)