# Generated by Django 4.2.7 on 2024-09-11 17:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nomina', '0005_remove_novedad_fecha_fin_remove_novedad_fecha_inicio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomina',
            name='fecha_nomina',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='novedad',
            name='fecha_ultima_actualizacion',
            field=models.DateField(blank=True, null=True),
        ),
    ]
