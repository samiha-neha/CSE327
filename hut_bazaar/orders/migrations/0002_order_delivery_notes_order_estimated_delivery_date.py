# Generated by Django 5.2 on 2025-04-11 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_notes',
            field=models.TextField(blank=True, help_text='Notes regarding delivery, like tracking links or delay reasons.', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='estimated_delivery_date',
            field=models.DateField(blank=True, help_text='Estimated date the order will be delivered.', null=True),
        ),
    ]
