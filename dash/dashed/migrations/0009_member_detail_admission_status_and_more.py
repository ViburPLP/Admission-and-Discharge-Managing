# Generated by Django 5.0.6 on 2024-07-29 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashed', '0008_alter_member_detail_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='member_detail',
            name='admission_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('admitted', 'Admitted'), ('discharged', 'Discharged')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='member_detail',
            name='status',
            field=models.CharField(max_length=100),
        ),
    ]
