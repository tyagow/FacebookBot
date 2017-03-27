from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from src.api.pedidos.serializers import PedidoCreateListSerializer
from src.pedidos.forms import PedidoForm
from src.pedidos.models import Pedido


class PedidoListView(ListView):
    model = Pedido

    def get_queryset(self):
        return Pedido.objects.realizados().hoje().order_by('-horario')

    def get_context_data(self, **kwargs):
        context = super(PedidoListView, self).get_context_data(**kwargs)
        # serializer = PedidoCreateListSerializer()
        # context['serializer'] = serializer
        form = PedidoForm()
        context['form'] = form
        return context

class PedidoDetailView(DetailView):
    model = Pedido


class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
