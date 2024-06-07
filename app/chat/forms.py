from django import forms
from django.core.exceptions import ValidationError
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        sender = cleaned_data.get('sender')
        thread = cleaned_data.get('thread')
        if sender and thread and not thread.participants.filter(id=sender.id).exists():
            raise ValidationError({'sender': 'The sender must be one of the participants in the thread.'})
        return cleaned_data
