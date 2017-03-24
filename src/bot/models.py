import datetime

from django.db import models
from django_fsm import FSMIntegerField, transition, can_proceed

from src.bot.managers import SessionManager
from src.bot.states import ClientStateEnum
from src.bot.utils import post_facebook_message, get_tokens
from src.pedidos.models import Pedido


SESSION_MINUTES_DURATION = 10


class Session(models.Model):
    state = FSMIntegerField(default=ClientStateEnum.ENVIAR_MENU)
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='sessions')
    last_active = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = SessionManager()

    def __str__(self):
        return '{} @ {}'.format(self.profile.first_name, self.last_updated)

    @property
    def fbid(self):
        return self.profile.fbid

    @property
    def endereco(self):
        return self.profile.endereco

    def is_expired(self):

        expired_date = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
        last_active = self.last_active.replace(tzinfo=None)
        return last_active <= expired_date

    def is_valid(self):
        if self.is_expired():
            self.active = False
            return False
        return True

    @property
    def last_updated(self):
        return self.last_active.astimezone().ctime()

    @transition(field=state, source='*', target=ClientStateEnum.PEDIDO_LISTA_PRODUTOS)
    def create_pedido(self):
        return self.pedidos.create(endereco=self.profile.endereco)

    def decode_msg(self, message):
        # print('State %s' % self.state)
        if self.state == ClientStateEnum.ENVIAR_MENU:
            self.send_menu()
        elif self.state == ClientStateEnum.RECEBER_OPCAO_MENU:
            self.read_menu(message)
        elif self.state == ClientStateEnum.PEDIDO:
            if can_proceed(self.update_or_create_pedido):
                self.update_or_create_pedido(message)
            else:
                self.send_cadastro_endereco()

        elif self.state == ClientStateEnum.CADASTRO_ENDERECO_RECEBER:
            self.update_endereco(message)
        elif self.state == ClientStateEnum.CADASTRO_TELEFONE:
            self.send_cadastro_telefone()
        elif self.state == ClientStateEnum.CADASTRO_TELEFONE_RECEBER:
            self.update_telefone(message)

        else:
            print('Unset STATE: %s' % self.state)

    def has_endereco(self):
        if len(self.profile.endereco) > 0:
            return True
        return False

    @transition(field=state, source='*',
                target=ClientStateEnum.PEDIDO_LISTA_PRODUTOS, conditions=[has_endereco])
    def update_or_create_pedido(self, message=None):
        pedido = Pedido.objects.filter(session=self).filter(active=True).first()
        if not pedido:
            pedido = self.create_pedido()

        if message:
            pedido.decode_message(message)
            print(pedido.get_state_display())

    def send_menu(self):
        post_facebook_message(self.fbid,
                              "Digite o numero da opção que voce deseja: \n1 - Fazer pedido \n2 - Meus Pedidos")
        self.set_state(ClientStateEnum.RECEBER_OPCAO_MENU)

    def send_cadastro_endereco(self):
        post_facebook_message(self.fbid,
                              'Por favor digite o endereço para realizarmos a entrega.')
        self.set_state(ClientStateEnum.CADASTRO_ENDERECO_RECEBER)

    def send_pedidos_ativos(self):
        post_facebook_message(self.fbid,
                              'Enviando pedidos que ainda não foram entregues.')
        for pedido in Pedido.objects.actives(self.profile.user):
            post_facebook_message(self.fbid,
                                  pedido.to_confirmation)

        self.set_state(ClientStateEnum.ENVIAR_MENU)
        self.send_menu()

    def send_cadastro_telefone(self):
        post_facebook_message(self.fbid,
                              'Por favor digite o telefone para entrarmos em contato.')
        self.set_state(ClientStateEnum.CADASTRO_TELEFONE_RECEBER)

    @transition(field=state, source='*', target=ClientStateEnum.CADASTRO_TELEFONE)
    def update_endereco(self, message):
        print('Updated endereco %s' % message)
        self.profile.endereco = message
        self.profile.save()
        self.set_state(ClientStateEnum.CADASTRO_TELEFONE)
        post_facebook_message(self.fbid, 'endereço atualizado!\nSeu novo endereço cadastrado é {}'.format(self.profile.endereco))
        self.send_cadastro_telefone()

    def update_telefone(self, message):
        print('Updated telefone %s' % message)
        self.profile.telefone = message
        self.profile.save()
        self.state = ClientStateEnum.ENVIAR_MENU
        self.save()
        post_facebook_message(self.fbid,
                              'telefone atualizado!\nSeu novo telefone cadastrado é {}'.format(self.profile.telefone))

        self.set_state(ClientStateEnum.PEDIDO)
        self.update_or_create_pedido('menu')

    def read_menu(self, message):
        tokens = get_tokens(message)
        if '1' in tokens:
            if can_proceed(self.update_or_create_pedido):
                self.state = ClientStateEnum.PEDIDO
                self.save()
                self.update_or_create_pedido(message)
            else:
                self.state = ClientStateEnum.CADASTRO_ENDERECO
                self.save()
                self.send_cadastro_endereco()
        elif '2' in tokens:
            self.send_pedidos_ativos()

        else:
            post_facebook_message(
                self.fbid,
                'Não entendi bem o que voce disse, pode repetir ?\nAinda estou aprendendo, desculpe...'
            )
            print('[read_menu] ESTADO - {} '.format(self.state))
            self.send_menu()

    def send_message(self, message):
        post_facebook_message(self.fbid, message)

    def set_state(self, state):
        self.state = state
        self.save()