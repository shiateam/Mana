# Generated by Django 3.2.7 on 2022-12-18 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20221218_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='store.brand'),
        ),
    ]
