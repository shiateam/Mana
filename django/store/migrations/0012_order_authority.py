# Generated by Django 3.2.7 on 2022-11-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_customer_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Authority',
            field=models.CharField(default=0, max_length=1100),
        ),
    ]