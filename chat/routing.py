from django.conf.urls import url

from chat.consumers import GroupChatConsumer, ChatConsumer

websocket_urls = [
    url(r'^ws/groups/$', GroupChatConsumer),  # after creating group by user
    url(r'^ws/chat/(?P<group_id>\d+)/$', ChatConsumer),  # user can enter to group
]