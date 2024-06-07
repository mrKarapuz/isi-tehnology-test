from rest_framework import serializers
from base.serializers import CustomUserSerializer
from chat.models import Thread
from chat.models import Message


class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = (
            'id',
            'created_at',
            'participants',
        )


class ThreadSerializer(ThreadCreateSerializer):
    participants = CustomUserSerializer(many=True)


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    is_read = serializers.ReadOnlyField()

    class Meta:
        model = Message
        fields = (
            'id',
            'created_at',
            'text',
            'is_read',
            'sender',
            'thread',
        )


class MarkAsReadSerializer(serializers.Serializer):
    is_read = serializers.BooleanField()


class UnreadMessageCountFilterSerializer(serializers.Serializer):
    sender = serializers.IntegerField(allow_null=True, required=False)
    thread = serializers.IntegerField(allow_null=True, required=False)


class UnreadMessageCountSerializer(serializers.Serializer):
    unread_message_count = serializers.IntegerField()
