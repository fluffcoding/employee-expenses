# Generated by Django 3.1.7 on 2021-02-27 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0013_remove_department_department_head'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, to='budget.department'),
        ),
    ]