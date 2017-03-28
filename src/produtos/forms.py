from django import forms

from src.produtos.models import Produto, ProductOrder


class ProductOrderForm(forms.ModelForm):
    # produtos = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Produto.objects.ativos())

    class Meta:
        model = ProductOrder
        fields = '__all__'
