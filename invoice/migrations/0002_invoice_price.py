# Generated by Django 4.0.3 on 2022-03-17 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
