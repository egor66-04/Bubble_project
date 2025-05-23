# Generated by Django 5.1.6 on 2025-04-24 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_achievement_achievement_type_achievement_emoji_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='max_points',
            field=models.PositiveIntegerField(default=10, verbose_name='Максимальное количество очков'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='time_limit',
            field=models.PositiveIntegerField(default=10, verbose_name='Ограничение по времени (мин)'),
        ),
    ]
