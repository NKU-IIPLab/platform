import json

import jwt
from asgiref.sync import sync_to_async
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# Websocket
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import connections, close_old_connections
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework_jwt.authentication import jwt_decode_handler

from app.models import Channel


class MessageChannel(AsyncWebsocketConsumer):
    async def connect(self):
        print(type(self.scope['user']), type(AnonymousUser()))
        if 'user' in self.scope and type(self.scope['user']) != type(AnonymousUser()):
            user = await self.scope['user']
        else:
            await self.disconnect(0)
            return

        print(self.channel_name)

        self.close_old_connections()
        client, created = await database_sync_to_async(Channel.objects.get_or_create)(user_id=user.id)
        client.channel_name = self.channel_name
        await database_sync_to_async(client.save)()

        await self.accept()

    @staticmethod
    def close_old_connections():
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()

    async def disconnect(self, code):
        self.close_old_connections()
        channels = await database_sync_to_async(Channel.objects.filter)(channel_name=self.channel_name)
        await database_sync_to_async(channels.delete)()

    async def receive(self, text_data=None, bytes_data=None):
        token = self.scope['cookies']['token']
        msg = json.loads(text_data)['msg']
        if msg == 'close':
            await self.disconnect(1)

    async def send_status(self, event):
        msg = event['msg']
        await self.send(text_data=json.dumps({'msg': msg}))


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        if b'cookie' not in headers:
            return self.inner(scope)
        token = headers[b'cookie']
        try:
            sync_to_async(close_old_connections)()

            token = token.decode().split('=')[1]
            payload = check_payload(token)
            user = check_user(payload)
            scope['user'] = user
        except exceptions.AuthenticationFailed:
            scope['user'] = AnonymousUser()
        return self.inner(scope)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))


# 检查负载
def check_payload(token):
    payload = None
    try:
        payload = jwt_decode_handler(token)
    except jwt.ExpiredSignature:
        msg = _('Signature has expired.')
        raise exceptions.AuthenticationFailed(msg)
    except jwt.DecodeError:
        msg = _('Error decoding signature.')
        raise exceptions.AuthenticationFailed(msg)

    return payload


# 检查用户
def check_user(payload, ):
    username = None
    User = get_user_model()
    try:
        username = payload.get('username')
    except Exception:
        msg = _('Invalid payload.')
        raise exceptions.AuthenticationFailed(msg)
    if not username:
        msg = _('Invalid payload.')
        raise exceptions.AuthenticationFailed(msg)
        # Make sure user exists
    try:
        user = database_sync_to_async(User.objects.get)(username=username)
    except User.DoesNotExist:
        msg = _("User doesn't exist.")
        raise exceptions.AuthenticationFailed(msg)

    return user
