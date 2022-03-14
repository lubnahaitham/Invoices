# Generated by Django 4.0.3 on 2022-03-14 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(blank=True, max_length=100, null=True)),
                ('item_name_in_arabic', models.CharField(blank=True, max_length=200, null=True)),
                ('item_name', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(blank=True, max_length=300, null=True)),
                ('building_number', models.IntegerField(blank=True, null=True)),
                ('street_name', models.CharField(blank=True, max_length=150, null=True)),
                ('district', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=300, null=True)),
                ('country', models.CharField(blank=True, max_length=300, null=True)),
                ('postal_code', models.IntegerField(blank=True, null=True)),
                ('additional_number', models.CharField(blank=True, max_length=150, null=True)),
                ('vat_number', models.IntegerField(blank=True, null=True)),
                ('other_seller_id', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
    ]
