# Generated by Django 5.0.6 on 2024-10-07 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bottel', '0012_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.BooleanField(default=False),
        ),
    ]
