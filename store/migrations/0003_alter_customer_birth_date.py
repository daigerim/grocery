# Generated by Django 4.2.7 on 2023-11-12 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_category_country_manufacturer_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
