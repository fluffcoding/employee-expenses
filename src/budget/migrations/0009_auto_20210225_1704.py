# Generated by Django 3.1.7 on 2021-02-25 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0008_auto_20210225_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
