# Generated by Django 5.0.2 on 2024-02-10 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_user_avatar_alter_coursematerial_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursefeedback',
            old_name='user',
            new_name='author',
        ),
    ]
