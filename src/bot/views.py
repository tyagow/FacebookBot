import json
import random
import re
from pprint import pprint

import requests
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

# from src.accounts.models import Profile
from django.contrib.auth.models import User


jokes = {
    'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
               """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
    'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
               """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
    'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
               """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]
}


def read_user_details(fbid):
    user_details_url = "https://graph.facebook.com/v2.8/{}?access_token={}".format(
        fbid,
        settings.FACEBOOK_BOT_ACCESS_TOKEN,
        # 'id,first_name,gender,'
    )
    print(user_details_url)
    return requests.get(user_details_url).json()



def decode_message(recevied_message, profile):
    pass



def read_message(fbid, recevied_message):
    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', recevied_message).lower().split()
    response_text = ''
    profile = None #Profile.objects.filter(fbid=fbid)
    if not profile:
        user_details = read_user_details(fbid)
        user = User.objects.create_user(username=fbid, password='cliente_password')
        user.profile.save_details(user_details)
        response_text = 'Oi {}, agora que já guardei teu nome na minha memória, podemos começar.\nEm que posso te ajudar?'.format(user.profile.first_name)

    else:
        response_text = decode_message(recevied_message, profile)

    return response_text


def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    token = settings.FACEBOOK_BOT_ACCESS_TOKEN
    post_message_url = 'https://graph.facebook.com/v2.8/me/messages?access_token={}'.format(token)
    response_msg = json.dumps({
        "recipient": {"id": fbid},
        "message": {"text": recevied_message}
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


class MyBotView(generic.View):

    # The get method is the same as before.. omitted here for brevity
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        print(self.request.body.decode('utf-8'))
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        print('Incoming message {}'.format(incoming_message))
        for entry in incoming_message['entry']:
            print('Entry message {}'.format(entry))
            for message in entry['messaging']:
                print('messaging {}'.format(message))
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    # print('Message: ', message)
                    id = message['sender']['id']
                    msg = message['message']['text']
                    if not id == settings.FACEBOOK_PAGE_ID:
                        msg = read_message(id, msg)
                        post_facebook_message(id, msg)
                    else:
                        print('Mensagem vinda de {id} e com o conteudo:{msg} não processada'.format(msg=msg, id=id))

        return HttpResponse()