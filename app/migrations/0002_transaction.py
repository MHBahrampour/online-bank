# Generated by Django 4.0.3 on 2022-04-26 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_card', models.CharField(max_length=16)),
                ('amount', models.CharField(max_length=12)),
                ('description', models.CharField(max_length=50)),
                ('cvv2', models.CharField(max_length=4)),
                ('second_pass', models.CharField(max_length=7)),
                ('atm_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.bankaccount')),
            ],
        ),
    ]