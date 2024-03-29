# Generated by Django 5.0.1 on 2024-01-27 12:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Zа-яА-яёЁіІїЇ]{1,20}$', 'First letter uppercase min 2 max 20 ch')])),
                ('surname', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Zа-яА-яёЁіІїЇ]{1,20}$', 'First letter uppercase min 2 max 20 ch')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
    ]
