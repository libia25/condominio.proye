# Generated by Django 5.1 on 2025-01-12 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0025_factura_saldo_pendiente'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factura',
            old_name='saldo_pendiente',
            new_name='saldo_pendienteF',
        ),
        migrations.RenameField(
            model_name='pago',
            old_name='saldo_pendiente',
            new_name='saldo_pendienteP',
        ),
    ]
