# Generated by Django 3.2.7 on 2022-11-14 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20221110_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='post',
            field=models.PositiveIntegerField(default=8971975755),
            preserve_default=False,
        ),
    ]
