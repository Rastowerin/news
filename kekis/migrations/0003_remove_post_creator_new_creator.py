# Generated by Django 5.0.4 on 2024-04-16 13:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kekis', '0002_alter_post_likes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='creator',
        ),
        migrations.AddField(
            model_name='new',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_news', to=settings.AUTH_USER_MODEL),
        ),
    ]
