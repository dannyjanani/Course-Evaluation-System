# Generated by Django 2.0.3 on 2018-04-26 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eval', '0005_auto_20180426_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='evalsession',
            name='session_eval_pswd',
            field=models.CharField(default='', max_length=15),
        ),
    ]