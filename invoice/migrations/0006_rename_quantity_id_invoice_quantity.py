# Generated by Django 4.0.3 on 2022-03-17 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_rename_quantity_invoice_quantity_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='quantity_id',
            new_name='quantity',
        ),
    ]
