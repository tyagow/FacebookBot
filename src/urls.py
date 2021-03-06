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

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n'))
]

urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('src.accounts.urls',  namespace='accounts')),
    url(r'^bot/', include('src.bot.urls',  namespace='bot')),
    url(r'^pedidos/', include('src.pedidos.urls',  namespace='pedido')),
    url(r'^api/pedidos/', include("src.api.pedidos.urls", namespace='pedidos-api')),
    url(r'^', include('src.core.urls',  namespace='core')),
]
