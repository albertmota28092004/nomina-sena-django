# Generated by Django 5.0.6 on 2024-06-13 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomina', '0020_alter_novedad_salario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomina',
            name='fecha_fin',
        ),
        migrations.RemoveField(
            model_name='nomina',
            name='fecha_inicio',
        ),
    ]