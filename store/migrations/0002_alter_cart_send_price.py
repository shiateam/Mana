# Generated by Django 3.2.7 on 2023-07-13 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='send_price',
            field=models.DecimalField(decimal_places=3, default=38000.0, error_messages={'name': {'max_length': 'The price must be between 0 and 999.999.'}}, help_text='Maximum 999.999', max_digits=12, verbose_name='Send Price'),
        ),
    ]