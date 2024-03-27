# Generated by Django 5.0.2 on 2024-02-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=255, unique=True)),
                ('app_source', models.CharField(max_length=255, null=True)),
                ('user_id', models.CharField(max_length=255, null=True)),
                ('password', models.CharField(max_length=255, null=True)),
                ('user_key', models.CharField(max_length=255, null=True)),
                ('encryption_key', models.CharField(max_length=255, null=True)),
                ('token', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
