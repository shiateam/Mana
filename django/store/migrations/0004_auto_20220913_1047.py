# Generated by Django 3.2.7 on 2022-09-13 06:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(default=django.utils.timezone.now, max_length=550),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(default=django.utils.timezone.now, max_length=225),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='province',
            field=models.CharField(default=django.utils.timezone.now, max_length=225),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productspecificationvalue',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productSpecificationValue', to='store.product'),
        ),
    ]
