from django.contrib import admin


# Register your models here.
from chat.models import GroupParticipant, ChatMessage, ChatGroup


@admin.register(GroupParticipant)
class GroupParticipantAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    pass
