# Generated by Django 3.1.6 on 2021-02-05 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcdashadmin', '0003_remove_employee_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
