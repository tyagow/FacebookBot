from django import forms

from src.produtos.models import Produto, ProductOrder


class ProductOrderForm(forms.ModelForm):
    produto = forms.ModelChoiceField(queryset=Produto.objects.ativos())
    # amount = forms.
    class Meta:
        model = ProductOrder
        exclude = ['id', 'pedido']