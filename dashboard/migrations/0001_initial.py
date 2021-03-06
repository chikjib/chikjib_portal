# Generated by Django 4.0.2 on 2022-03-29 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PortalWebhookMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateTimeField(help_text='When we received the event.')),
                ('payload', models.JSONField(default=None, null=True)),
            ],
        ),
        migrations.AddIndex(
            model_name='portalwebhookmessage',
            index=models.Index(fields=['received_at'], name='dashboard_p_receive_d0ffd0_idx'),
        ),
    ]
