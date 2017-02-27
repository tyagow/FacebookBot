from django.conf.urls import url

from src.core import views
from src.core import views as core_views


urlpatterns = [
    url(r'^$', views.home, name='home'),
]
