from channels.generic.websocket import AsyncJsonWebsocketConsumer


class BaseChatCinsumer(AsyncJsonWebsocketConsumer):

    #msg from user>reddis>receive_json>_group_send>channel_layer>response_proxy>to all users in group with name self.channel
    async def _group_send(self, data, event=None):
        data = {'type': 'response.proxy', 'data': data, 'event': event}
        await self.channel_layer.group_send(self.channel, data)  # self.channel ints group name

    async def response_proxy(self, event):
        await self._send_message(event['data'], event=event.get('event'))

    async def _send_message(self, data, event=None):
        await self.send_json(content={'status': 'ok', 'data': data, 'event': event})

    async def _throw_error(self, data, event=None):
        await self.send_json(content={'status': 'error', 'data': data, 'event': event})

    async def connect(self):
        "Check if user is login or send error and close connection"
        await self.accept()
        if 'user' not in self.scope or self.scope['user'].is_anonymous:
            await self._send_message({'detail': 'Authorization failed'})
            await self.close(code=1000)
            return

    async def receive_json(self, content, **kwargs):
        message = await self.parse_content(content)
        if message:
            event = message['event'].replace('.', '_')  # find handler
            method = getattr(self, f'event_{event}', self.method_undefined)  # get method in object(self in class) or method_undefined
            await method(message)
        else:
            await self._throw_error({'detail': 'Invalid message'})

    async def method_undefined(self, message):
        "If cant find method in class"
        await self._throw_error({'detail': 'Unknown event'}, event=message['event'])

    @classmethod
    async def parse_content(cls, content):
        "Check json content"
        if isinstance(content, dict) and isinstance(content.get('event'), str) and isinstance(content.get('data'), dict):
            return content