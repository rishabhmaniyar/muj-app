# Generated by Django 5.0.2 on 2024-03-24 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='levels',
            name='symbol',
            field=models.CharField(max_length=255),
        ),
    ]
