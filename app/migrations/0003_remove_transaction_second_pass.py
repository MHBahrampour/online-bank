# Generated by Django 4.0.3 on 2022-04-26 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='second_pass',
        ),
    ]