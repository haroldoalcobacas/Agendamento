# Generated by Django 5.1.5 on 2025-02-03 18:31

import django.core.validators
import django.db.models.deletion
import medicos.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('crm', models.CharField(max_length=200, verbose_name='CRM')),
                ('telefone', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="O número precisa estar neste formato:                     '+99 99 9999-0000'.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Telefone')),
                ('especialidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicos', to='medicos.especialidade')),
            ],
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.DateField(help_text='Insira uma data para agenda', validators=[medicos.models.validar_dia])),
                ('horario', models.CharField(choices=[('1', '07:00 ás 08:00'), ('2', '08:00 ás 09:00'), ('3', '09:00 ás 10:00'), ('4', '10:00 ás 11:00'), ('5', '11:00 ás 12:00')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agenda', to='medicos.medico')),
            ],
            options={
                'unique_together': {('horario', 'dia')},
            },
        ),
    ]
