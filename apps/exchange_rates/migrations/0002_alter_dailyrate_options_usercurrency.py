# Generated by Django 4.2.4 on 2023-09-22 05:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exchange_rates', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dailyrate',
            options={'ordering': ['-date']},
        ),
        migrations.CreateModel(
            name='UserCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold', models.FloatField(default=1)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exchange_rates.currency')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
