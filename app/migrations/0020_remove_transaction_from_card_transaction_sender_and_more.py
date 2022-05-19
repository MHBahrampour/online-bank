# Generated by Django 4.0.3 on 2022-05-19 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_rename_to_card_transaction_recipient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='from_card',
        ),
        migrations.AddField(
            model_name='transaction',
            name='sender',
            field=models.CharField(default='sender', max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='recipient',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('Transfer', 'Transfer'), ('Recharge', 'Recharge'), ('Charity', 'Charity')], max_length=8),
        ),
    ]
