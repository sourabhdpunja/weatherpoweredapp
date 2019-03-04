# Generated by Django 2.1.7 on 2019-03-04 01:27

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailCredentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailId', models.CharField(default='', max_length=120)),
                ('location', models.CharField(default='', max_length=200)),
                ('latitude', models.DecimalField(decimal_places=10, default=Decimal('0.0000'), max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=10, default=Decimal('0.0000'), max_digits=10)),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]