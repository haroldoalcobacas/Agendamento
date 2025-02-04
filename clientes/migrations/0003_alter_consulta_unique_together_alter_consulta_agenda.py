# Generated by Django 5.1.5 on 2025-02-04 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_consulta_agenda_alter_consulta_cliente'),
        ('medicos', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='consulta',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='consulta',
            name='agenda',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='consulta', to='medicos.agenda'),
        ),
    ]
