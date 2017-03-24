from rest_framework.serializers import ModelSerializer

from src.pedidos.models import Pedido


class PedidoUpdateSerializer(ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'status',
        ]

#
# class PedidoCreateSerializer(ModelSerializer):
#     class Meta:
#         model = Pedido
#         fields = [
#             'status',
#         ]
#


class PedidoDetailSerializer(ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'client_name',
            'horario',
            'endereco',
            'entrega',
            'get_entrega_display',
            'produtos',
            'status',
            'get_status_display',
            'valor_total',
        ]


class PedidoListSerializer(ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'pk',
            'client_name',
            'horario',
            'endereco',
            'entrega',
            'get_entrega_display',
            'produtos',
            'status',
            'get_status_display',
            'valor_total',
        ]
