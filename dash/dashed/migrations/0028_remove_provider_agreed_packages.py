# Generated by Django 5.0.6 on 2024-11-12 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashed', '0027_remove_scheme_policy_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='agreed_packages',
        ),
    ]
