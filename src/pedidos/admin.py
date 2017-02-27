from django.contrib import admin

# Register your models here.
from src.pedidos.models import Pedido
from src.produtos.models import ProductOrder


class ProdutosTabularInlineAdmin(admin.TabularInline):
    model = ProductOrder
    extra = 0
    readonly_fields = ['valor_total_text']

    def valor_total_text(self, obj):
        return 'R$ {}'.format(obj.valor_total)

    valor_total_text.short_description = 'Total'


class PedidoAdmin(admin.ModelAdmin):
    inlines = [ProdutosTabularInlineAdmin]


admin.site.register(Pedido, PedidoAdmin)