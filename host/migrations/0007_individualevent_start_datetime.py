# Generated by Django 5.0.6 on 2025-02-25 06:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0006_individualevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualevent',
            name='start_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
