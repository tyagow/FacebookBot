from django.conf.urls import url, include

from src.core import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
