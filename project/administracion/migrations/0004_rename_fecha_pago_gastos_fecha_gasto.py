# Generated by Django 5.1.4 on 2025-01-06 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0003_remove_gastos_fijo_variable_remove_gastos_mes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gastos',
            old_name='fecha_pago',
            new_name='fecha_gasto',
        ),
    ]