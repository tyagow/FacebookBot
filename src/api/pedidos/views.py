from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)

from src.pedidos.models import Pedido
from .serializers import (
    PedidoDetailSerializer,
    PedidoListSerializer,
    # PedidoCreateUpdateSerializer
    PedidoUpdateSerializer)

#
# class PedidoCreateAPIView(CreateAPIView):
#     queryset = Pedido.objects.all()
#     serializer_class = PedidoCreateUpdateSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class PedidoDetailAPIView(RetrieveAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoDetailSerializer
    lookup_field = 'pk'
    # lookup_url_kwarg = 'another_name_than_slug_example'


class PedidoDeleteAPIView(DestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoDetailSerializer
    lookup_field = 'pk'


class PedidoListAPIView(ListAPIView):
    queryset = Pedido.objects.hoje().realizados()
    serializer_class = PedidoListSerializer


class PedidoUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoUpdateSerializer
    lookup_field = 'pk'

    # def perform_update(self, serializer):
    #     serializer.save(user=self.request.user)
