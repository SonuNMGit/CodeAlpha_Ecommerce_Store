# Generated by Django 5.0.6 on 2024-10-07 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bottel', '0013_order_delivery_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='estimated_delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
