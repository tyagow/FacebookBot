from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMIntegerField

from src.bot.states import ClientStateEnum
from src.bot.utils import get_tokens
from src.produtos.models import Produto

STATUS_CHOICES = (
    (1, 'Aberto'),
    (2, 'Realizado'),
    (3, 'Enviado'),
    (4, 'Finalizado'),
)


class PedidoState(object):
    ABERTO = 1
    LISTA_PRODUTOS = 20
    SELECIONAR_PRODUTO = 50
    ADICIONAR_MAIS_PRODUTOS = 55
    QUANTIDADE_PRODUTO = 60
    ENDERECO_ENTREGA = 80
    OBSERVACAO = 100
    CONFIRMAR_PEDIDO = 120
    FINALIZADO  = 200


class Pedido(models.Model):
    """
    Pedido must be created by a Session

    """
    session = models.ForeignKey('bot.Session', related_name='pedidos')
    endereco = models.CharField(max_length=100)
    observacao = models.TextField(blank=True)
    status = models.IntegerField(_('Status'), choices=STATUS_CHOICES, default=1)
    state = FSMIntegerField(default=PedidoState.ABERTO)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '#{id} - {autor}  Total R$ {total}'.format(
            id=self.id,
            autor=self.session.profile.first_name,
            total=self.produtos.total(self)
        )

    def decode_message(self, message):
        print('Pedido decode message %s' % message)
        print('Pedido state %s' % self.state)
        if self.state == PedidoState.ABERTO:
            self.send_produtos()
        elif self.state == PedidoState.LISTA_PRODUTOS:
            self.send_produtos()
        elif self.state == PedidoState.SELECIONAR_PRODUTO:
            self.read_produto(message)
        elif self.state == PedidoState.ADICIONAR_MAIS_PRODUTOS:
            self.adicionar_mais_produto(message)
        elif self.state == PedidoState.QUANTIDADE_PRODUTO:
            self.quantidade_produto(message)
        elif self.state == PedidoState.ENDERECO_ENTREGA:
            self.endereco_entrega(message)
        elif self.state == PedidoState.OBSERVACAO:
            self.read_observacao(message)
        elif self.state == PedidoState.CONFIRMAR_PEDIDO:
            self.confirmar_pedido(message)

    def send_produtos(self):
        lista_produtos = Produto.objects.ativos()
        # lista_produtos = map(lambda x: x.nome, lista_produtos)
        lista = 'Lista de produtos:\n'
        for produto in lista_produtos:
            if produto in self.produtos.list_produtos(self):
                lista += '{id} - {nome} - R$ {valor} - No carrinho\n'.format(
                                                                        id=produto.id,
                                                                        nome=produto.nome,
                                                                        valor=produto.valor
                )
            else:
                lista += '{id} - {nome} - R$ {valor}\n'.format(id=produto.id, nome=produto.nome, valor=produto.valor)
        lista += 'Selecione um produto, só preciso do numero do produto...\n:)'
        self.state = PedidoState.SELECIONAR_PRODUTO
        self.save()
        self.session.send_message(lista)

    def read_produto(self, message):

        produto = None
        id = None
        try:
            id = int(message)
            produto = Produto.objects.filter(id=id).first()
        except:
            pass
        print(id)

        if produto:
            self.produto = self.produtos.create(produto=produto, amount=0)
            print(self.produto.amount)
            self.session.send_message('Produto {} adicionado com sucesso.'.format(produto.nome))
            self.session.send_message('Qual a quantidade que voce deseja?.')
            self.set_state(PedidoState.QUANTIDADE_PRODUTO)
        else:
            self.session.send_message('Não encontrei este produto... Por favor digite somente o numero do produto desejado.')
            self.send_produtos()

    def adicionar_mais_produto(self, message):
        if 'sim' in message:
            self.send_produtos()
        else:
            self.set_state(PedidoState.ENDERECO_ENTREGA)
            self.session.send_message('Posso usar teu endereço cadastrado ou gostarias de adicionar um endenreço de entrega diferente? Responda sim ou o endereço')

    def quantidade_produto(self, message):
        produto = self.produtos.filter(amount=0).first()
        print('quantidade produto %s' % self.produtos.all().first().amount)
        print('quantidade produto %s' % message)
        try:
            quantidade = int(message)
            produto.set_amount(quantidade)
            produto.save()
            self.session.send_message(
                '{qnt}  {produto} adicionado ao seu pedido,'.format(
                    produto=produto.nome,
                    qnt=produto.amount,
                    total=produto.valor_total
                )
            )
            self.session.send_message(
                'Voce gostaria de adicionar mais algum produto ? \nResponda sim ou não.'
            )
            self.set_state(PedidoState.ADICIONAR_MAIS_PRODUTOS)
        except:
            self.session.send_message(
                'Não entendi esta quantidade, por favor diga somente quantos {} voce quer.'.format(produto.nome)
            )

    def endereco_entrega(self, message):
        if message[:3] == 'sim':
            self.endereco_entrega(self.session.endereco)
        else:
            self.set_endereco(message)
            self.set_state(PedidoState.OBSERVACAO)
            self.session.send_message('Voce gostaria de adicionar alguma observação no pedido ? Digite não ou diga sua obervação.')

    def set_endereco(self, endereco):
        self.endereco = endereco

    def read_observacao(self, message):
        if not message[:3] == 'nao' or message[:3] == 'não':
            self.observacao = message
        self.set_state(PedidoState.CONFIRMAR_PEDIDO)

    def set_state(self, state):
        if state == PedidoState.CONFIRMAR_PEDIDO:
            self.send_confirmation()

        self.state = state
        self.save()

    def set_edereco(self, endereco):
        self.endereco = endereco

    @property
    def to_confirmation(self):
        text = "Seu Pedido:\n"
        text += '-----------\n'
        text += 'Pedido aberto em {}\n'.format(self.timestamp)
        text += 'Produtos:\n'
        text += '-----------\n'

        for produto in self.produtos.all():
            text += '{qnt} - {nome} - valor: {valor}'.format(qnt=produto.amount, nome=produto.nome, valor=produto.valor)

        text += '-----------\n'
        text += 'Total: R$ {}\n'.format(self.produtos.total(pedido=self))
        text += '-----------\n'
        text += 'Entrega: {}\n'.format(self.endereco)
        text += 'Observação: {}\n'.format(self.observacao)

        return text

    def send_confirmation(self):
        self.session.send_message(self.to_confirmation)
        self.session.send_message('Voce confirma este pedido? Digite sim ou não.')

    def confirmar_pedido(self, message):
        if 'sim' in message[:3]:
            self.status = 2
            self.active = False
            self.set_state(PedidoState.FINALIZADO)
            self.session.send_message('Pedido Confirmado!\nObrigado pela preferencia!')
            self.session.set_state(ClientStateEnum.ENVIAR_MENU)
            self.session.send_menu()
        else:
            self.set_state(PedidoState.LISTA_PRODUTOS)

    @property
    def last_updated_tz(self):
        return self.last_updated.astimezone().ctime()