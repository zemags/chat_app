from django.db import models
from django.contrib.auth import get_user_model


class ChatGroup(models.Model):
    name = models.CharField(max_length=255, default='')  # group name from user

    @property
    def link(self):
        channel_name = self.channel_name(self.id)
        return f'/ws/chat/{channel_name}/'

    def __str__(self):
        return self.name

    @classmethod
    def channel_name(cls, group_id):
        # group_name for channel_layer like group_{group_id}
        return f'group_{group_id}'


class GroupParticipant(models.Model):
    user = models.ForeignKey(
        get_user_model(),  # user model
        related_name='group_user',
        on_delete=models.CASCADE,
        null=True
    )
    group = models.ForeignKey(
        ChatGroup,
        related_name='group_participant',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.user.username


class ChatMessage(models.Model):
    #  link to user who added message
    user = models.ForeignKey(
        get_user_model(),
        related_name='user_message',
        on_delete=models.CASCADE,
        null=True
    )
    # link to group where the message
    group = models.ForeignKey(
        ChatGroup,
        related_name='group_message',
        on_delete=models.CASCADE,
        null=True
    )
    message = models.TextField(default='')

    def __str__(self):
        return self.message

