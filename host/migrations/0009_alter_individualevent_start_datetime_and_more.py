# Generated by Django 5.0.6 on 2025-02-27 09:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0008_individualevent_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualevent',
            name='start_datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='IndividualEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='host.individualevent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
