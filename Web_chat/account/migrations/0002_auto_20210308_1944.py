# Generated by Django 3.1.7 on 2021-03-08 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='date_joine',
            new_name='date_joined',
        ),
    ]