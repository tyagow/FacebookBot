import json

from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from src.bot.utils import read_message, post_facebook_message


class MyBotView(generic.View):

    # The get method is the same as before.. omitted here for brevity
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '2318934571':
            return HttpResponse(self.request.GET['hub.challenge'])

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        # print('Incoming message {}'.format(incoming_message))
        for entry in incoming_message['entry']:
            # print('Entry message {}'.format(entry))
            for message in entry['messaging']:
                # print('messaging {}'.format(message))
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    # print('Message: ', message)
                    id = message['sender']['id']
                    print(id)

                    msg = message['message']['text']
                    if not id == settings.FACEBOOK_PAGE_ID:
                        read_message(id, msg)
                    # else:
                    #     print('Mensagem vinda de {id} e com o conteudo:{msg} não processada'.format(msg=msg, id=id))

        return HttpResponse('teste')