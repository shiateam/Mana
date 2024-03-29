# Generated by Django 3.2.7 on 2023-04-18 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_alter_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='send_price',
            field=models.DecimalField(decimal_places=3, default=380.0, error_messages={'name': {'max_length': 'The price must be between 0 and 999.999.'}}, help_text='Maximum 999.999', max_digits=6, verbose_name='Send Price'),
        ),
    ]
