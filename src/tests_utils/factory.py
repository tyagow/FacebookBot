import factory
from django.conf import settings
from django.contrib.auth.models import User

from src.accounts.models import Profile
from src.bot.models import Session


class UserFactory(factory.Factory):
    class Meta:
        model = User

    first_name = 'John'
    last_name = 'Doe'


class ProfileFactory(factory.Factory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)


class SessionFactory(factory.Factory):
    class Meta:
        model = Session

    profile = factory.SubFactory(ProfileFactory)




