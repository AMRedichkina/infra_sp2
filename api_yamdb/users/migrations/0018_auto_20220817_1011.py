# Generated by Django 2.2.16 on 2022-08-17 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20220813_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_moderator',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'Обычный пользователь'), ('moderator', 'Модератор'), ('admin', 'Админ'), ('superuser', 'Суперюзер')], default='user', max_length=9),
        ),
    ]
