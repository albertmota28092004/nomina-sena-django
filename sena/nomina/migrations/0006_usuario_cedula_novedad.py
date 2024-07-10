# Generated by Django 5.0.6 on 2024-06-11 19:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomina', '0005_alter_usuario_cargo'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cedula',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='Novedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('clase_salario', models.IntegerField(choices=[(1, 'Básico'), (2, 'Integral')], default=1)),
                ('dias_incapacidad', models.IntegerField()),
                ('dias_trabajados', models.IntegerField()),
                ('horas_extras_diurnas', models.IntegerField(blank=True, null=True)),
                ('horas_extras_diurnas_dom_fes', models.IntegerField()),
                ('horas_extras_nocturnas', models.IntegerField()),
                ('horas_extras_nocturnas_dom_fes', models.IntegerField()),
                ('horas_recargo_nocturno', models.IntegerField()),
                ('horas_recargo_nocturno_dom_fes', models.IntegerField()),
                ('horas_recargo_diurno_dom_fes', models.IntegerField()),
                ('comisiones', models.IntegerField(blank=True, null=True)),
                ('comisiones_porcentaje', models.CharField(blank=True, max_length=256, null=True)),
                ('bonificaciones', models.IntegerField(blank=True, null=True)),
                ('embargos_judiciales', models.IntegerField(blank=True, null=True)),
                ('libranzas', models.IntegerField(blank=True, null=True)),
                ('cooperativas', models.IntegerField(blank=True, null=True)),
                ('otros', models.IntegerField(blank=True, null=True)),
                ('riesgo', models.IntegerField(choices=[(1, 'Riesgo I'), (2, 'Riesgo II'), (3, 'Riesgo III'), (4, 'Riesgo IV'), (5, 'Riesgo V')])),
                ('riesgo_porcentaje', models.CharField(max_length=256)),
                ('fecha_ingreso', models.DateField()),
                ('fecha_fin_contrato', models.DateField()),
                ('tipo_contrato', models.IntegerField(choices=[(1, 'Término fijo inferior a 1 año'), (2, 'Término fijo superior a 1 año'), (3, 'Contrato por obra y labor'), (4, 'Contrato indefinido')])),
                ('fecha_retiro', models.DateField(blank=True, null=True)),
                ('motivo_retiro', models.CharField(blank=True, max_length=256, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomina.usuario')),
            ],
        ),
    ]
