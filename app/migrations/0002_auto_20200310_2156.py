# Generated by Django 3.0.1 on 2020-03-10 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='order_notes',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
