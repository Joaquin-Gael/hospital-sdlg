# Generated by Django 5.0.6 on 2024-08-31 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0004_servicios_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicios',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]
