# Generated by Django 5.1 on 2024-12-29 22:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0007_alter_pago_residente'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='facturas',
            field=models.ManyToManyField(related_name='pagos', to='condominio.factura'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='pago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factura_asociada', to='condominio.pago'),
        ),
    ]
