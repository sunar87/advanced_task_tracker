# Generated by Django 4.2.19 on 2025-02-22 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customtelegramuser',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]
