# Generated by Django 4.0.4 on 2022-10-11 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_auth', '0006_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='user_avatars'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cover',
            field=models.ImageField(blank=True, upload_to='user_covers'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]