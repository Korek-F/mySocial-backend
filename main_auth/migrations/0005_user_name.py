# Generated by Django 4.0.4 on 2022-06-14 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_auth', '0004_alter_user_avatar_alter_user_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]