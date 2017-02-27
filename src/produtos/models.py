from django.db import models
from django.utils.translation import ugettext_lazy as _


class ProdutoManager(models.Manager):
    def ativos(self, **kwargs):
        return super(ProdutoManager, self).filter(active=True)


class Produto(models.Model):
    nome = models.CharField(_('Produto'), max_length=120)
    valor = models.FloatField(_('Valor'), max_length=10)
    active = models.BooleanField('Ativa', default=True)

    objects = ProdutoManager()

    def __str__(self):
        return self.nome


class ProductOrderManager(models.Manager):
    def total(self, pedido):
        total = 0
        for p in super(ProductOrderManager, self).filter(pedido=pedido):
            total += p.valor_total
        return total

    def list_produtos(self, instance):
        list_orders = super(ProductOrderManager, self).filter(pedido=instance)
        produtos = []
        for p in list_orders:
            produtos.append(p.produto)
        return produtos


class ProductOrder(models.Model):
    amount = models.IntegerField('Quantidade',default=0)
    produto = models.ForeignKey('Produto', related_name='pedidos')
    pedido = models.ForeignKey('pedidos.Pedido', related_name='produtos')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = ProductOrderManager()

    def set_amount(self, quantidade):
        self.amount = quantidade

    def __str__(self):
        return '{} {} - R${}'.format(self.amount, self.nome, self.valor_total)

    @property
    def last_updated_tz(self):
        return self.last_updated.astimezone().ctime()

    @property
    def valor_total(self):
        return float(self.produto.valor) * self.amount

    @property
    def nome(self):
        return self.produto.nome

    @property
    def valor(self):
        return self.produto.valor