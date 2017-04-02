import datetime
from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from src.pedidos.models import Pedido
from src.produtos.models import ProductOrder, Produto


class PedidoUpdateSerializer(ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'status',
        ]


class ProductOrderDetailSerializer(ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = [
            'amount',
            'nome',
            'valor',
            'valor_total'
        ]


class ProdutoCreateSerializer(ModelSerializer):
    class Meta:
        model = Produto
        fields = [
            'nome',
        ]


class ProductOrderCreateSerializer(ModelSerializer):
    produto = ProdutoCreateSerializer(Produto.objects.ativos(), many=True).data
    
    class Meta:
        model = ProductOrder
        fields = [
            'amount',
            'produto',
        ]
    
    def create(self, validated_data):
        print(validated_data)


class PedidoCreateSerializer(ModelSerializer):
    horario = serializers.DateTimeField(input_formats=['%d/%m/%Y %H:%M', '%H:%M'], default=(timezone.now() - datetime.timedelta(hours=3)))
    # produtos = ProductOrderCreateSerializer(many=True).data

    class Meta:
        model = Pedido
        fields = [
            'produtos',
            'cliente',
            'entrega',
            'endereco',
            'origin',
            'horario',
            'observacao',
            'status'

        ]

    def create(self, validated_data):
        print('DATA %s' % validated_data)
        # print(dir(self))
        produtos_data = validated_data.pop('produtos')
        horario = validated_data.pop('horario')
        # print(produtos_data)
        from django.utils import timezone
        today = timezone.now() - datetime.timedelta(hours=3)
        # print(today)
        # print(horario)
        # print(dir(horario))
        horario = horario - datetime.timedelta(minutes=6)
        hora = horario.hour

        if horario < today:
            horario = horario.replace(day=today.day, year=today.year, month=today.month)
        # validated_data.pop('amount')
        # validated_data.pop('produto')
        # print(horario)
        # print(validated_data)
        pedido = Pedido.objects.create(**validated_data)
        pedido.horario = horario
        pedido.save()
        # print(validated_data.data.get('produtos-TOTAL_FORMS'))
        # for produto in produtos_data:
        #     print(produto.nome)
        return pedido


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
        return ProductOrderDetailSerializer(obj.produtos.all(), many=True, read_only=True).data


class PedidoListSerializer(ModelSerializer):
    produtos = ProductOrderDetailSerializer(many=True)
    
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

