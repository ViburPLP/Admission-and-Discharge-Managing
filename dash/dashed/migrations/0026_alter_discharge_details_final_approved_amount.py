# Generated by Django 5.0.6 on 2024-11-10 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashed', '0025_alter_discharge_details_final_approved_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discharge_details',
            name='final_approved_amount',
            field=models.CharField(max_length=100),
        ),
    ]