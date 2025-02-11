# Generated by Django 5.1 on 2024-12-30 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0012_rename_usuario_departamento_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='facturas',
            field=models.ManyToManyField(blank=True, related_name='pagos', to='condominio.factura'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha_emision',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pago',
            name='monto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='pago',
            name='servicios',
            field=models.ManyToManyField(blank=True, to='condominio.servicio'),
        ),
    ]
