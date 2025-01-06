from django.contrib.auth.models import User
from django.db import models


class Conversation(models.Model):
    SENDER_CHOICES = (
        ('user', 'User'),
        ('bot', 'Bot'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['session_id']),
        ]

    def __str__(self):
        return f"Conversation by {self.user or self.session_id} at {self.timestamp}"
