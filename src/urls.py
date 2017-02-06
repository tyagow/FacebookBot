"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

from src.core import views as core_views
from src.core.views import MyBotView

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n'))
]

urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('src.accounts.urls',  namespace='accounts')),
    url(r'^$', core_views.home, name='home'),
    url(r'^66d2b8f4a09cd35cb23076a1da5d51529136a3373fd570b122/?$', MyBotView.as_view()),
    url('', include('social_django.urls', namespace='social'))
]
