from django.conf.urls import url, include

from src.bot.views import MyBotView


urlpatterns = [
    url(r'^66d2b8f4a09cd35cb23076a1da5d51529136a3373fd570b122/?$', MyBotView.as_view(), name='main'),
]
