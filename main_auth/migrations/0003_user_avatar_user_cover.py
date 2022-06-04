# Generated by Django 4.0.4 on 2022-06-03 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_auth', '0002_remove_user_friends_user_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='user_avatars'),
        ),
        migrations.AddField(
            model_name='user',
            name='cover',
            field=models.ImageField(blank=True, upload_to='user_covers'),
        ),
    ]
