# Generated by Django 4.0.3 on 2022-05-21 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_transaction_rem_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.PositiveBigIntegerField(),
        ),
    ]
