# Generated by Django 5.0.6 on 2024-11-12 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashed', '0029_payer_providerpanel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payer',
        ),
        migrations.DeleteModel(
            name='ProviderPanel',
        ),
    ]