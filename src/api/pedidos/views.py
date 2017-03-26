from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView, ListCreateAPIView)

from src.pedidos.models import Pedido
from .serializers import (
    PedidoDetailSerializer,
    PedidoListSerializer,
    # PedidoCreateUpdateSerializer
    PedidoUpdateSerializer, PedidoCreateSerializer)


class PedidoCreateAPIView(CreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoCreateSerializer

    def perform_create(self, serializer):
        serializer.save()


class PedidoDetailAPIView(RetrieveAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoDetailSerializer
    lookup_field = 'pk'
    # lookup_url_kwarg = 'another_name_than_slug_example'


class PedidoDeleteAPIView(DestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoDetailSerializer
    lookup_field = 'pk'


class PedidoListAPIView(ListCreateAPIView):
    queryset = Pedido.objects.hoje().realizados()
    serializer_class = PedidoListSerializer


class PedidoUpdateAPIView(UpdateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoUpdateSerializer
    lookup_field = 'pk'

