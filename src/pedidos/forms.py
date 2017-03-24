from django import forms

from src.pedidos.models import Pedido


class PedidoForm(forms.ModelForm):
    # empresa = forms.ModelChoiceField(
    #     queryset=Empresa.objects.filter_sem_representante(),
    #     empty_label="---",
    #     label=_('Selecione uma empresa para ser representante')
    # )
    #
    class Meta:
        model = Pedido
        fields = '__all__'
