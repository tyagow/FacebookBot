from django import forms

from src.pedidos.models import Pedido


class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = '__all__'
