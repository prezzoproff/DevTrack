# Generated by Django 5.1.6 on 2025-03-03 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='status',
            field=models.CharField(choices=[('open', 'open'), ('In progres', 'In progres'), ('Closed', 'Closed')], default='open', max_length=20),
        ),
    ]
