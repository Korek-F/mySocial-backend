# Generated by Django 4.0.4 on 2022-08-28 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_auth', '0005_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]