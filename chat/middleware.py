from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.utils.functional import LazyObject

User = get_user_model()


class MyLazyObject(LazyObject):
    def _setup(self):
        raise ValueError("Accessing scope obj brefore it is ready")


class MyMiddleware(BaseMiddleware):
    @database_sync_to_async
    def _get_user(self):
        return User.objects.all().first()

    def populate_scope(self, scope):  # BaseMiddleware method - sync method
        # define vars in scope
        # scope['my_var'] = MyLazyObject()
        scope['my_var'] = 'Hello'

    async def resolver_scope(self, scope):
        scope['my_var']._wrapped = await self._get_user()  # fill mylazyobject vars, and get user from db


class SimpleMiddleware:
    # own middleware
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return self.inner(dict(scope, my_var='hello'))  # on any cinsumer in scope will be my_var


MyMiddlewareStack = lambda inner: AuthMiddlewareStack(MyMiddleware(inner))

SimpleMiddlewareStack = lambda inner: AuthMiddlewareStack(SimpleMiddleware(inner))
