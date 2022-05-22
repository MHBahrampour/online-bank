# Generated by Django 4.0.3 on 2022-05-17 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_transaction_account_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='atm_card',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.bankaccount', to_field='atm_card'),
        ),
    ]