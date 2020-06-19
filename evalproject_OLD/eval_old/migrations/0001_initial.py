# Generated by Django 2.0.3 on 2018-03-22 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('prof_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('prof_pswd', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('stud_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('stud_pswd', models.CharField(max_length=30)),
            ],
        ),
    ]