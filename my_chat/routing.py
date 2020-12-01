#  request by web sockets

from channels.routing import ProtocolTypeRouter, URLRouter

from chat.routing import websocket_urls

from chat.middleware import SimpleMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': SimpleMiddlewareStack(URLRouter(websocket_urls)),
    # create own middleware websocket - protocol name, URLRouter accept url for websockets
})
