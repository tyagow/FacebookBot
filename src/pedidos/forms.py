from django import forms

from src.pedidos.models import Pedido
from src.produtos.models import Produto


class PedidoForm(forms.ModelForm):
    produtos = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Produto.objects.ativos())
    observacao = forms.CharField(widget=forms.Textarea(attrs={'cols': 15, 'rows': 4}))

    class Meta:
        model = Pedido
        fields = ['cliente', 'produtos', 'endereco', 'horario', 'entrega', 'status', 'observacao']
        exclude = ['session', 'state', 'active', 'origin']
