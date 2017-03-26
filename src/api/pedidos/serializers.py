from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from src.pedidos.models import Pedido
from src.produtos.models import ProductOrder


class PedidoUpdateSerializer(ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'status',
        ]


class ProdutoPedidoSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields =[
            'amount',
            'nome',
            'valor',
            'valor_total'
        ]


class PedidoCreateSerializer(ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'origin',
            'state',
        ]

    def create(self, validated_data):
        return Pedido.objects.create(**validated_data)


class PedidoDetailSerializer(ModelSerializer):
    produtos = SerializerMethodField()

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
            'get_status_display',
            'valor_total',
        ]
        extra_kwargs = {'produtos': {'required': False}}

    def get_produtos(self, obj):
        return ProdutoPedidoSerializer(obj.produtos.all(), many=True, read_only=True).data


class PedidoListSerializer(ModelSerializer):
    produtos = ProdutoPedidoSerializer(many=True, read_only=True)
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
        extra_kwargs = {'produtos': {'required': False}}

