# Generated by Django 5.1 on 2024-12-29 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0004_mantenimiento_departamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='monto_pagado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
