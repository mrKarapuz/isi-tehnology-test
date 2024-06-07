from django.db import models
from base.models import User


class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(User, related_name='threads')

    def __str__(self):
        participants = self.participants.all()
        participant_names = [str(participant) for participant in participants]
        return f'{str(self.id)}: ' + ' - '.join(participant_names) if participant_names else 'No participants'


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f'Message from {self.sender} ({self.id})'

    class Meta:
        ordering = ('created_at',)
