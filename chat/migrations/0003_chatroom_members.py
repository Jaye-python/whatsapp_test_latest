# Generated by Django 4.2.6 on 2023-12-01 12:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatroom_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
