# Generated by Django 5.0 on 2024-10-19 17:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0007_horario_medicos_servicioid'),
        ('turnero', '0002_citas_fecha_citas_fecha_created_citas_userid_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModelTurnos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horarioID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicos.horario_medicos')),
                ('medicoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicos.medicos')),
                ('servicioID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicos.servicios')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
