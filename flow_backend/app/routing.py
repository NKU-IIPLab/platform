from django.urls import path

from app.websocket import MessageChannel

websocket_urlpatterns = [
    path('message', MessageChannel),
]