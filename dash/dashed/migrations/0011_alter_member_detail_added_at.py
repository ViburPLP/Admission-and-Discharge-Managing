# Generated by Django 5.0.6 on 2024-07-29 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashed', '0010_alter_member_detail_added_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member_detail',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
