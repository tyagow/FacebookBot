import json
import re
from pprint import pprint

import requests
from django.conf import settings
from django.contrib.auth.models import User

from src.accounts.models import Profile


def read_user_details(fbid):
    user_details_url = "https://graph.facebook.com/v2.8/{}?access_token={}".format(
        fbid,
        settings.FACEBOOK_BOT_ACCESS_TOKEN,
        # 'id,first_name,gender,'
    )
    return requests.get(user_details_url).json()


def get_or_create_profile(fbid):
    profile = Profile.objects.filter(fbid=fbid).first()
    created = False
    if not profile:
        created = True
        user_details = read_user_details(fbid)
        user = User.objects.create_user(username=fbid, password='cliente_password')
        user.profile.save_details(fbid, user_details)
        user.profile.update_or_create_session()
        post_facebook_message(fbid, 'Olá {nome}, vejo que está é a primeira vez que nos falamos, que legal!')

    return created, profile


def decode_message(recevied_message, profile):
    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', recevied_message).lower().split()
    print(tokens)


def read_message(fbid, recevied_message):
    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', recevied_message).lower().split()
    response_text = ''
    created, profile = get_or_create_profile(fbid)
    if not created:
        session_created, session = profile.update_or_create_session()
        if session_created:
            print('Sessao Criada')
            print(recevied_message)
        else:
            print('Sessão ativa')
            print(recevied_message)
        # profile.session.decode_msg(recevied_message)


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

