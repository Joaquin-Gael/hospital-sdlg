# Generated by Django 5.0 on 2024-07-31 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departamentos',
            fields=[
                ('departamentoID', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ubicaciones',
            fields=[
                ('ubicacionID', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidades',
            fields=[
                ('especialidadID', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=25)),
                ('descripcion', models.CharField(max_length=255)),
                ('departamentoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicos.departamentos')),
            ],
        ),
        migrations.CreateModel(
            name='Medicos',
            fields=[
                ('medicoID', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('especialidadID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicos.especialidades')),
            ],
        ),
        migrations.CreateModel(
            name='Horario_medicos',
            fields=[
                ('horarioID', models.AutoField(primary_key=True, serialize=False)),
                ('dia', models.CharField(max_length=100)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('departamentoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicos.departamentos')),
                ('especialidadID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicos.especialidades')),
                ('medicoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicos.medicos')),
            ],
        ),
        migrations.AddField(
            model_name='departamentos',
            name='ubicacionID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicos.ubicaciones'),
        ),
    ]