# Generated by Django 5.0.6 on 2024-06-07 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomina', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cargo',
            field=models.IntegerField(choices=[(1, 'Almacenista'), (2, 'Analista de ingeniería'), (3, 'Aprendiz etapa lectiva'), (4, 'Aprendiz etapa práctica'), (5, 'Auditor'), (6, 'Auxiliar contable'), (7, 'Auxiliar de almacén'), (8, 'Auxiliar de bodega'), (9, 'Auxiliar de calidad'), (10, 'Auxiliar de diseño'), (11, 'Auxiliar de gestión humana'), (12, 'Auxiliar de ingeniería'), (13, 'Auxiliar de mecánica'), (14, 'Auxiliar de servicios generales'), (15, 'Coordinador de área'), (16, 'Despachador'), (17, 'Diseñadora'), (18, 'Domiciliario'), (19, 'Gerente'), (20, 'Jefe de calidad'), (21, 'Jefe de compras'), (22, 'Jefe de despachos'), (23, 'Jefe de Gestión Humana'), (24, 'Jefe de planta'), (25, 'Mecánico'), (26, 'Operario de corte'), (27, 'Operario de empaque'), (28, 'Operario de extendido'), (29, 'Operario de máquina'), (30, 'Operario de máquinas especiales'), (31, 'Operario de muestras'), (32, 'Operario de terminación'), (33, 'Operario manual'), (34, 'Patinador'), (35, 'Patronista'), (36, 'Recepcionista'), (37, 'Revisora'), (38, 'Secretaria'), (39, 'Supervisor'), (40, 'Vigilante'), (41, 'No aplica')], default=41),
        ),
    ]