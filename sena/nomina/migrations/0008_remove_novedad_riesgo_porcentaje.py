# Generated by Django 5.0.6 on 2024-06-11 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomina', '0007_alter_novedad_dias_incapacidad_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novedad',
            name='riesgo_porcentaje',
        ),
    ]
