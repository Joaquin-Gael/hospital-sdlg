# Generated by Django 5.0 on 2024-10-15 02:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0006_rename_hora_fin_horario_medicos_hora_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario_medicos',
            name='servicioID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='medicos.servicios'),
            preserve_default=False,
        ),
    ]
