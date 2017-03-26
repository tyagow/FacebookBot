import datetime

import pytz
from django.db import models
from django.shortcuts import resolve_url
from django.utils.translation import ugettext_lazy as _
from django_fsm import FSMIntegerField

from src.bot.states import ClientStateEnum
from src.pedidos.managers import PedidoModelManager
from src.pedidos.utils import check_back_menu_action, isDateTimeFormat, isTimeFormat
from src.produtos.models import Produto

STATUS_CHOICES = (
    (1, 'Aberto'),
    (2, 'Realizado'),
    (3, 'Enviado'),
    (4, 'Finalizado'),
    (5, 'Abandonado'),
)
TIPO_ENTREGA_CHOICES = (
    (1, 'MotoBoy'),
    (2, 'Retirar no local'),
)
ORIGIN_CHOICES = (
    (1, 'Facebook'),
    (2, 'Loja'),
)
STATE_CHOICES = (
    (1, 'Aberto'),
    (20, 'Lista de Produtos'),
    (50, 'Selecionando Produto'),
    (55, 'Adicionando Mais Produtos'),
    (60, 'Quantidade do produto'),
    (70, 'Tipo de Entrega'),
    (75, 'Horario'),
    (80, 'Endereco para entrega'),
    (100, 'Observação'),
    (120, 'Confirmando pedido'),
    (200, 'Pedido Feito'),
)

PEDIDO_ABERTO = 1
PEDIDO_REALIZADO = 2
PEDIDO_ENVIADO = 3
PEDIDO_FINALIZADO = 4
PEDIDO_ABANDONADO = 5


class PedidoState(object):
    ABERTO = 1
    LISTA_PRODUTOS = 20
    SELECIONAR_PRODUTO = 50
    ADICIONAR_MAIS_PRODUTOS = 55
    QUANTIDADE_PRODUTO = 60
    TIPO_ENTREGA = 70
    HORARIO = 75
    ENDERECO_ENTREGA = 80
    OBSERVACAO = 100
    CONFIRMAR_PEDIDO = 120
    FINALIZADO  = 200


class Pedido(models.Model):
    """
    Pedido can be created by a Session

    """
    session = models.ForeignKey('bot.Session', related_name='pedidos', null=True, blank=True)
    endereco = models.CharField(max_length=100, blank=True)
    observacao = models.TextField(blank=True)
    status = models.IntegerField(_('Status'), choices=STATUS_CHOICES, default=1)
    state = FSMIntegerField(default=PedidoState.ABERTO, choices=STATE_CHOICES)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)
    entrega = models.IntegerField(_('Tipo entrega'), choices=TIPO_ENTREGA_CHOICES, default=1)
    horario = models.DateTimeField(_('Horario'), blank=True, null=True)
    origin = models.IntegerField(_('Origem Pedido'), choices=ORIGIN_CHOICES, default=1)
    objects = PedidoModelManager()
    cliente = models.CharField(max_length=100, blank=True)

    def __str__(self):
        autor = '?'
        if self.session:
            # Pedido vindo do Facebook
            autor = self.session.profile.first_name

        return '#{id} - {autor} @ {hora}  Total R$ {total}'.format(
            id=self.id,
            autor=autor,
            total=self.produtos.total(self),
            hora=self.horario_verbose
        )

    def get_absolute_url(self):
        return resolve_url('pedido:detail', pk=self.pk)

    def decode_message(self, message):
        # print('Pedido decode message %s' % message)
        # print('Pedido state %s' % self.state)
        if self.status == PEDIDO_ABANDONADO:
            self.send_recuperar_pedido(message)
        elif self.state == PedidoState.ABERTO:
            self.send_produtos()
        elif self.state == PedidoState.LISTA_PRODUTOS:
            self.send_produtos()
        elif self.state == PedidoState.SELECIONAR_PRODUTO:
            self.read_produto(message)
        elif self.state == PedidoState.ADICIONAR_MAIS_PRODUTOS:
            self.adicionar_mais_produto(message)
        elif self.state == PedidoState.QUANTIDADE_PRODUTO:
            self.quantidade_produto(message)
        elif self.state == PedidoState.TIPO_ENTREGA:
            self.tipo_entrega(message)
        elif self.state == PedidoState.HORARIO:
            self.read_horario(message)
        elif self.state == PedidoState.ENDERECO_ENTREGA:
            self.endereco_entrega(message)
        elif self.state == PedidoState.OBSERVACAO:
            self.read_observacao(message)
        elif self.state == PedidoState.CONFIRMAR_PEDIDO:
            self.confirmar_pedido(message)

    def send_produtos(self):
        lista_produtos = Produto.objects.ativos()
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
        lista += 'Selecione um produto pelo numero\n'
        lista += 'Ou digite menu para abandonar este pedido e voltar para o menu\n'
        self.state = PedidoState.SELECIONAR_PRODUTO
        self.save()
        self.session.send_message(lista)

    def read_produto(self, message):
        if check_back_menu_action(message):
            self.back_menu()
            return
        produto = None
        _id = None
        try:
            _id = int(message)
            produto = Produto.objects.filter(id=_id).first()
        except:
            pass
        # print(_id)

        if produto:
            self.produto = self.produtos.create(produto=produto, amount=0)
            # print(self.produto.amount)
            self.session.send_message('Produto {} adicionado com sucesso.'.format(produto.nome))
            self.session.send_message('Qual a quantidade que voce deseja?')
            self.set_state(PedidoState.QUANTIDADE_PRODUTO)
        else:
            self.session.send_message('Não encontrei este produto... Por favor digite somente o numero do produto desejado.')
            self.send_produtos()

    def adicionar_mais_produto(self, message):
        if 'sim' in message.lower():
            self.send_produtos()
        else:
            self.set_state(PedidoState.TIPO_ENTREGA)
            self.session.send_message('Seleciona a forma de entrega:\n1 - Motoboy\n2 - Retirar no local')

    def quantidade_produto(self, message):
        produto = self.produtos.filter(amount=0).first()
        # print('quantidade produto %s' % self.produtos.all().first().amount)
        # print('quantidade produto %s' % message)
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

    def tipo_entrega(self, message):
        try:
            tipo_entrega= int(message)
            if tipo_entrega in [1,2]:
                self.entrega = tipo_entrega
                self.set_state(PedidoState.ENDERECO_ENTREGA)
                self.session.send_message(
                    'Entrega selecionada: {}'.format(self.get_entrega_display())
                )
                if tipo_entrega == 1:
                    self.set_state(PedidoState.ENDERECO_ENTREGA)
                    msg = 'Posso usar o seu endereço cadastrado? Digite sim ou o endereço de entrega deste pedido.'
                else:
                    self.set_state(PedidoState.HORARIO)
                    msg = 'Diga a hora que voce deseja este pedido:\nExemplo: 12:30'

                self.session.send_message(msg)


            else:
                self.session.send_message('Não entendi este tipo de entrega.')
        except:
            self.session.send_message('Não entendi este tipo de entrega.')

    def endereco_entrega(self, message):
        if message[:3].lower() == 'sim':
            self.endereco_entrega(self.session.endereco)
        else:
            self.set_endereco(message)
            self.set_state(PedidoState.HORARIO)
            self.session.send_message(
                'Diga a hora que voce deseja este pedido.\nExemplo: 12:30')

    def set_endereco(self, endereco):
        self.endereco = endereco

    def read_horario(self, message):
        if isTimeFormat(message) or isDateTimeFormat(message):
            self.set_horario(message)
            self.set_state(PedidoState.OBSERVACAO)
            self.session.send_message(
                'Hora do pedido:\n {}\n--------------\nVoce gostaria de adicionar alguma observação no pedido ?\nDigite não ou diga sua obervação.'.format(self.horario_verbose)
            )
        else:
            self.session.send_message(
                'Por favor digite o horario no formato 12:15 (HH:MM)')

    def read_observacao(self, message):
        if not message[:3].lower() == 'nao' or message[:3].lower() == 'não':
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
        text += 'Pedido aberto em {}\n'.format(self.last_updated_tz)
        text += 'Produtos:\n'
        text += '-----------\n'

        for produto in self.produtos.all():
            text += '({qnt}) {nome}\nvalor: {valor}\n'.format(qnt=produto.amount, nome=produto.nome, valor=produto.valor)
            text += '-----------\n'

        text += 'Total: R$ {}\n'.format(self.produtos.total(pedido=self))
        text += '-----------\n'
        text += 'Entrega: {}\n'.format(self.get_entrega_display())
        text += 'Endereco: {}\n'.format(self.endereco) if self.entrega == 1 else ''
        text += 'Horario: {}\n'.format(self.horario_verbose)
        text += 'Observação: {}\n'.format(self.observacao)

        return text

    def send_confirmation(self):
        self.session.send_message(self.to_confirmation)
        self.session.send_message('Voce confirma este pedido? Digite sim ou não.')

    def confirmar_pedido(self, message):
        if 'sim' in message[:3].lower():
            self.status = 2
            self.active = False
            self.set_state(PedidoState.FINALIZADO)
            self.session.send_message('Pedido Confirmado!\nObrigado pela preferencia!')
            self.session.set_state(ClientStateEnum.RECEBER_OPCAO_MENU)
            self.session.send_menu()
        else:
            self.session.send_message('Pedido Cancelado.\n')
            self.back_menu()

    def back_menu(self):
        self.status = PEDIDO_ABANDONADO
        self.active = False
        self.save()
        self.session.set_state(ClientStateEnum.RECEBER_OPCAO_MENU)
        self.session.send_menu()



    @property
    def last_updated_tz(self):
        return self.last_updated.astimezone().strftime('%d/%m/%Y %H:%M')

    @property
    def valor_total(self):
        return self.produtos.total(self)

    @property
    def horario_verbose(self):
        if self.horario:
            return self.horario.astimezone().strftime('%d/%m/%Y %H:%M')
        else:
            return '----'

    @property
    def horario_hora(self):
        return self.horario.astimezone().strftime('%H:%M')

    @property
    def telefone(self):
        return self.session.profile.telefone

    def set_horario(self, data):
        d = datetime.datetime.now()
        _data = data if isDateTimeFormat(data) else '{}/{}/{} {}'.format(d.day, d.month, d.year, data)
        horario = datetime.datetime.strptime(_data, '%d/%m/%Y %H:%M')
        self.horario = pytz.timezone('America/Sao_Paulo').localize(horario)
        self.save()

    @property
    def client_name(self):
        return self.session.profile.first_name