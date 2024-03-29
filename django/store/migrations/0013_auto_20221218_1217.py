# Generated by Django 3.2.7 on 2022-12-18 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_order_authority'),
    ]

    operations = [
        migrations.AddField(
            model_name='productspecification',
            name='brand',
            field=models.CharField(default='سایر', help_text='Required', max_length=255, verbose_name='brand'),
        ),
        migrations.AlterField(
            model_name='productspecification',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='typeSpecification', to='store.producttype'),
        ),
        migrations.AlterField(
            model_name='productspecificationvalue',
            name='specification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='specificationValue', to='store.productspecification'),
        ),
    ]
