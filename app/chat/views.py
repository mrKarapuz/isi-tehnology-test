from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import GenericViewSet
from chat.models import Thread
from chat.models import Message
from chat.serializers import ThreadCreateSerializer
from chat.serializers import ThreadSerializer
from chat.serializers import MessageSerializer
from chat.serializers import MarkAsReadSerializer
from chat.serializers import UnreadMessageCountSerializer
from chat.serializers import UnreadMessageCountFilterSerializer


@extend_schema(tags=['threads'])
class ThreadView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    model = Thread
    serializer_class = ThreadSerializer
    serializer_action_classes = {
        'create': ThreadCreateSerializer,
        'update': ThreadCreateSerializer,
    }
    queryset = Thread.objects.all()
    http_method_names = (
        'post',
        'get',
        'put',
        'delete',
    )
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication, JWTAuthentication]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('created_at',)
    filterset_fields = ('participants',)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Thread.objects.all()
        return Thread.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).prefetch_related('participants')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        participants.append(self.request.user.pk)
        if participants:
            existing_threads = Thread.objects.annotate(
                num_participants=Count('participants')
            ).filter(
                num_participants=len(participants)
            ).distinct()
            for thread in existing_threads:
                thread_participants = set(thread.participants.values_list('id', flat=True))
                if set(participants) == thread_participants:
                    serializer = self.get_serializer(thread)
                    return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)


@extend_schema(tags=['messages'])
class MessageView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    model = Message
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    http_method_names = (
        'post',
        'get',
        'put',
        'patch',
        'delete',
    )
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication, JWTAuthentication]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ('text',)
    filterset_fields = ('sender', 'thread', 'is_read',)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Message.objects.all()
        return Message.objects.none()

    def perform_create(self, serializer):
        return serializer.save(sender=self.request.user)

    @extend_schema(
        request=MarkAsReadSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        description='Update the read status of a message by ID.'
    )
    @action(['patch'], detail=True, url_path='read')
    def mark_as_read(self, request, *args, **kwargs):  # noqa
        try:
            message = self.get_object()
            serializer = MarkAsReadSerializer(data=request.data)
            serializer.is_valid()
            message.is_read = serializer.validated_data.get('is_read')
            message.save()
            return Response(status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='sender',
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name='thread',
                type=OpenApiTypes.INT,
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: UnreadMessageCountSerializer(),
        },
        description='Get unread count of unread messages'
    )
    @action(['get'], detail=False, url_path='unread')
    def get_unread_messages_count(self, request, *args, **kwargs):  # noqa
        serializer = UnreadMessageCountFilterSerializer(data=request.query_params)
        if serializer.is_valid():
            sender = serializer.validated_data.get('sender')
            thread = serializer.validated_data.get('thread')
            messages = Message.objects.filter(is_read=False)
            if sender:
                messages = messages.filter(sender=sender)
            if thread:
                messages = messages.filter(thread=thread)
            serializer = UnreadMessageCountSerializer({
                'unread_message_count': messages.count()
            })
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)