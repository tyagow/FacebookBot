import datetime
from django.utils import timezone
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


class ProductOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = [
            'amount',
            'nome',
            'valor',
            'valor_total'
        ]


class PedidoCreateSerializer(ModelSerializer):
    horario = serializers.DateTimeField(input_formats=['%d/%m/%Y %H:%M', '%H:%M'], default=(timezone.now() - datetime.timedelta(hours=3)))
    produso = ProductOrderSerializer()
    class Meta:
        model = Pedido
        fields = [
            'origin',
            'status',
            'cliente',
            'endereco',
            'produtos',
            'horario',
            'entrega',
            'observacao'
        ]

    def create(self, validated_data):
        produtos_data = validated_data.pop('produtos')
        horario = validated_data.pop('horario')
        from django.utils import timezone
        today = timezone.now() - datetime.timedelta(hours=3)
        # print(today)
        # print(horario)
        # print(dir(horario))
        if horario < today:
            horario = horario.replace(day=today.day, year=today.year, month=today.month, minute=horario.minute-6)

        # print(horario)

        pedido = Pedido.objects.create(**validated_data)
        pedido.horario = horario
        pedido.save()
        for produto in produtos_data:
            print(produto)
        return pedido

    def get_produtos(self, obj):
        return ProductOrderSerializer(obj.produtos.all(), many=True, read_only=True).data


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
        return ProductOrderSerializer(obj.produtos.all(), many=True, read_only=True).data


class PedidoListSerializer(ModelSerializer):
    produtos = ProductOrderSerializer(many=True)
    
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

