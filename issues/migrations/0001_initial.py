# Generated by Django 5.1.6 on 2025-03-02 22:02

import _io
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('priority', models.CharField(choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')], default='medium', max_length=20)),
                ('status', models.CharField(choices=[('open', 'open'), ('In progres', 'In progres'), ('Closed', 'Closed')], default=_io.open, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
