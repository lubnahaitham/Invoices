# Generated by Django 4.0.3 on 2022-03-17 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_invoice_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='quantity',
            new_name='td_quantity',
        ),
    ]