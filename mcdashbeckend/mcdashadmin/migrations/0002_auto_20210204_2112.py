# Generated by Django 3.1.6 on 2021-02-05 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcdashadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='store_number',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
