# Generated by Django 5.1.4 on 2025-03-29 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_alter_usuarios_cargado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='cargado',
            field=models.DateField(auto_now_add=True),
        ),
    ]
