# Generated by Django 5.0.2 on 2024-02-15 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_user_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='picture',
        ),
    ]
