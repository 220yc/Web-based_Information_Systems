# Generated by Django 3.2.18 on 2023-06-11 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0004_alter_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='subtotal',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
