# Generated by Django 3.2.15 on 2022-09-05 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-id']},
        ),
    ]
