# Generated by Django 3.2.7 on 2023-04-07 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True)),
                ('validation_code', models.CharField(blank=True, max_length=5, null=True)),
                ('time_created', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
