# Generated by Django 4.2.13 on 2024-06-07 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("text", models.TextField()),
                ("is_read", models.BooleanField(default=False)),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "thread",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="chat.thread",
                    ),
                ),
            ],
        ),
    ]
