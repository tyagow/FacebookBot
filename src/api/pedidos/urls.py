from django.conf.urls import url

from .views import (
    PedidoCreateAPIView,
    PedidoListAPIView,
    PedidoDetailAPIView,
    PedidoDeleteAPIView,
    PedidoUpdateAPIView
)

urlpatterns = [
    url(r'^$', PedidoListAPIView.as_view(), name='list'),
    url(r'^create/$', PedidoCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>[\w-]+)/$', PedidoDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>[\w-]+)/edit/$', PedidoUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<pk>[\w-]+)/delete/$', PedidoDeleteAPIView.as_view()),
]
