from django.contrib import admin

from chat.forms import MessageForm
from chat.models import Thread
from chat.models import Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    search_fields = (
        'participants__email__icontains',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    form = MessageForm

    list_display = (
        'id',
        'created_at',
        'short_text',
        'is_read',
        'sender',
        'thread',
    )

    list_display_links = (
        'created_at',
        'short_text',
    )
    list_filter = (
        'is_read',
        'sender',
    )

    def short_text(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text

    short_text.short_description = 'Text'
