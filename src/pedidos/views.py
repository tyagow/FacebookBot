# Create your views here.
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from src.pedidos.forms import PedidoForm
from src.pedidos.models import Pedido
from src.produtos.forms import ProductOrderForm
from src.produtos.models import ProductOrder


class PedidoListView(ListView):
    model = Pedido

    def get_queryset(self):
        return Pedido.objects.all() # realizados().hoje().order_by('-horario')

    def get_context_data(self, **kwargs):
        context = super(PedidoListView, self).get_context_data(**kwargs)
        # serializer = PedidoCreateListSerializer()
        # context['serializer'] = serializer
        form = PedidoForm()

        ProductOrderInlineFormSet = inlineformset_factory(Pedido, ProductOrder, form=ProductOrderForm,
                                                          fields=('amount', 'produto'), extra=1)
        formset = ProductOrderInlineFormSet()
        context['form'] = form
        context['formset'] = formset

        return context


class PedidoDetailView(DetailView):
    model = Pedido


class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm


def pedido_create(request):

    form = PedidoForm(request.POST or None, request.FILES or None)
    # form.fields['produtos'].queryset = ProductOrder.objects.all()
    ProductOrderInlineFormSet = inlineformset_factory(Pedido, ProductOrder, form=ProductOrderForm, fields=('amount', 'produto'), extra=1)
    formset = ProductOrderInlineFormSet(request.POST or None, request.FILES or None)

    if request.method == "POST":
        form = PedidoForm(request.POST)

        formset = ProductOrderInlineFormSet(request.POST or None)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "formset": formset,
    }
    return render(request, "pedidos/pedido_form.html", context)
