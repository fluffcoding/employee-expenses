# Generated by Django 3.1.7 on 2021-02-25 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='head',
            field=models.BooleanField(default=False),
        ),
    ]
