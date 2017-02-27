from django.contrib import admin

# Register your models here.
from src.produtos.models import Produto, ProductOrder


admin.site.register(Produto)
admin.site.register(ProductOrder)
