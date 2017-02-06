import json
import random
from pprint import pprint

import re
import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'core/index.html')

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
        settings.FACEBOOK_BOT_ACCESS_TOKEN
    )
    return requests.get(user_details_url).json()


def read_message(fbid, recevied_message):
    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', recevied_message).lower().split()
    joke_text = ''
    for token in tokens:
        if token in jokes:
            joke_text = random.choice(jokes[token])
            break
    if not joke_text:
        joke_text = "I didn't understand! Send 'stupid', 'fat', 'dumb' for a Yo Mama joke!"
    user_details = read_user_details(fbid)
    # user_details_params = {'access_token': ''}
    # "https://graph.facebook.com/v2.8/1418290114907670?access_token=EAAJFXZBZCsZCYIBAMigSNHrNE8azwy53AFr6TZAoRHZC0NEgiboVifjCTIan1tE0y7aLkOgIjsCxKSi3zrkQEY0Vip3sRPOfakaAIMubHdhfQhGBw4rxqSrYvAUIrA5TecnV4qkubJcwikoCoHp1bIhVnwZBweZBR1Jmow5bteKDAZDZD"
    joke_text = 'Yo ' + user_details['first_name'] + '..!' + joke_text

    return joke_text


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
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
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

        return HttpResponse()