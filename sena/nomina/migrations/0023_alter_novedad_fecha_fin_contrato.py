# Generated by Django 5.0.6 on 2024-06-13 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomina', '0022_nominaquincena'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novedad',
            name='fecha_fin_contrato',
            field=models.DateField(blank=True, null=True),
        ),
    ]