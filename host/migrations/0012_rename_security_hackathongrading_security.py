# Generated by Django 5.0.6 on 2025-03-02 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0011_hackathongrading'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hackathongrading',
            old_name='Security',
            new_name='security',
        ),
    ]
