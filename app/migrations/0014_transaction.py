# Generated by Django 4.0.3 on 2022-05-17 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_delete_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_card', models.CharField(blank=True, max_length=16)),
                ('amount', models.CharField(max_length=12)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=50)),
                ('atm_card', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.bankaccount')),
            ],
        ),
    ]
