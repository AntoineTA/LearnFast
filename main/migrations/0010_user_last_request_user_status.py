# Generated by Django 5.0.2 on 2024-02-13 21:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_request',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
