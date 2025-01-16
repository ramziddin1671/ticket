# Generated by Django 4.2.17 on 2024-12-26 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0010_ticket_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='accepted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
