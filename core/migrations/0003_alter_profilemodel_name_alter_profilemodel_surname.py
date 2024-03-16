# Generated by Django 5.0.1 on 2024-01-31 15:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_profilemodel_name_alter_profilemodel_surname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='name',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Zа-яА-яёЁіІїЇ]{2,20}$', 'First letter uppercase min 2 max 20 ch')]),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='surname',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Zа-яА-яёЁіІїЇ]{2,20}$', 'First letter uppercase min 2 max 20 ch')]),
        ),
    ]