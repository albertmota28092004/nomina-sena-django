# Generated by Django 5.0.6 on 2024-06-25 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomina', '0026_alter_usuario_cedula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novedad',
            name='bonificaciones',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='comisiones',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='comisiones_porcentaje',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='cooperativas',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='dias_incapacidad',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='embargos_judiciales',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='horas_extras_diurnas',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='horas_extras_diurnas_dom_fes',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='horas_extras_nocturnas',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='horas_extras_nocturnas_dom_fes',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='horas_recargo_diurno_dom_fes',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='horas_recargo_nocturno',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='horas_recargo_nocturno_dom_fes',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='libranzas',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='otros',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]