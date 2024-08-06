from django.db import models
from django.utils import timezone

from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Usuario(models.Model):
    ROLES = (
        (1, 'Administrador'),
        (2, 'Colaborador')
    )
    CARGOS = (
        (1, "No aplica"),
        (2, "Almacenista"),
        (3, "Analista de ingeniería"),
        (4, "Aprendiz etapa lectiva"),
        (5, "Aprendiz etapa práctica"),
        (6, "Auditor"),
        (7, "Auxiliar contable"),
        (8, "Auxiliar de almacén"),
        (9, "Auxiliar de bodega"),
        (10, "Auxiliar de calidad"),
        (11, "Auxiliar de diseño"),
        (12, "Auxiliar de gestión humana"),
        (13, "Auxiliar de ingeniería"),
        (14, "Auxiliar de mecánica"),
        (15, "Auxiliar de servicios generales"),
        (16, "Coordinador de área"),
        (17, "Despachador"),
        (18, "Diseñadora"),
        (19, "Domiciliario"),
        (20, "Gerente"),
        (21, "Jefe de calidad"),
        (22, "Jefe de compras"),
        (23, "Jefe de despachos"),
        (24, "Jefe de Gestión Humana"),
        (25, "Jefe de planta"),
        (26, "Mecánico"),
        (27, "Operario de corte"),
        (28, "Operario de empaque"),
        (29, "Operario de extendido"),
        (30, "Operario de máquina"),
        (31, "Operario de máquinas especiales"),
        (32, "Operario de muestras"),
        (33, "Operario de terminación"),
        (34, "Operario manual"),
        (35, "Patinador"),
        (36, "Patronista"),
        (37, "Recepcionista"),
        (38, "Revisora"),
        (39, "Secretaria"),
        (40, "Supervisor"),
        (41, "Vigilante"),
    )
    cedula = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=256)
    apellido = models.CharField(max_length=256)
    correo = models.EmailField(max_length=256)
    contrasena = models.CharField(max_length=256)
    foto = models.ImageField(null=True, blank=True, upload_to='fotos_usuarios')
    rol = models.PositiveIntegerField(choices=ROLES, default=2)
    cargo = models.PositiveIntegerField(null=True, blank=True, choices=CARGOS, default=1)
    fecha_ingreso = models.DateField(default=timezone.now)

    def get_cargo_display(self):
        return dict(self.CARGOS).get(self.cargo, "Cargo desconocido")

    def get_rol_display(self):
        return dict(self.ROLES).get(self.rol, "Rol desconocido")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Novedad(models.Model):
    CLASE_CONTRATO = (
        (1, "Término fijo inferior a 1 año"),
        (2, "Término fijo superior a 1 año"),
        (3, "Contrato por obra y labor"),
        (4, "Contrato indefinido")
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 2})
    salario = models.IntegerField()
    dias_incapacidad = models.PositiveIntegerField(null=True, blank=True, default=0)
    dias_trabajados = models.PositiveIntegerField()
    horas_extras_diurnas = models.PositiveIntegerField(null=True, blank=True, default=0)
    horas_extras_diurnas_dom_fes = models.PositiveIntegerField(null=True, blank=True, default=0)
    horas_extras_nocturnas = models.PositiveIntegerField(null=True, blank=True, default=0)
    horas_extras_nocturnas_dom_fes = models.PositiveIntegerField(null=True, blank=True, default=0)
    horas_recargo_nocturno = models.PositiveIntegerField(null=True, blank=True, default=0)
    horas_recargo_nocturno_dom_fes = models.PositiveIntegerField(null=True, blank=True, default=0)
    horas_recargo_diurno_dom_fes = models.PositiveIntegerField(null=True, blank=True, default=0)
    comisiones = models.PositiveIntegerField(null=True, blank=True, default=0)
    comisiones_porcentaje = models.FloatField(null=True, blank=True, default=0)
    bonificaciones = models.PositiveIntegerField(null=True, blank=True, default=0)
    embargos_judiciales = models.PositiveIntegerField(null=True, blank=True, default=0)
    libranzas = models.PositiveIntegerField(null=True, blank=True, default=0)
    cooperativas = models.PositiveIntegerField(null=True, blank=True, default=0)
    otros = models.PositiveIntegerField(null=True, blank=True, default=0)
    riesgo = models.FloatField(default=0)
    fecha_fin_contrato = models.DateField(null=True, blank=True)
    tipo_contrato = models.PositiveIntegerField(choices=CLASE_CONTRATO)
    fecha_retiro = models.DateField(null=True, blank=True)
    motivo_retiro = models.CharField(max_length=256, null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"{self.usuario} - {self.fecha_inicio} - {self.fecha_fin}"


class Devengado(models.Model):
    novedad = models.ForeignKey(Novedad, on_delete=models.CASCADE)

    @property
    def novedad_salario(self):
        return self.novedad.salario

    @property
    def novedad_dias_incapacidad(self):
        return self.novedad.dias_incapacidad or 0

    @property
    def novedad_dias_trabajados(self):
        return self.novedad.dias_trabajados

    @property
    def novedad_comisiones(self):
        return self.novedad.comisiones or 0

    @property
    def novedad_comisiones_porcentaje(self):
        return self.novedad.comisiones_porcentaje or 0

    @property
    def novedad_horas_extras_diurnas(self):
        return self.novedad.horas_extras_diurnas or 0

    @property
    def novedad_horas_extras_diurnas_dom_fes(self):
        return self.novedad.horas_extras_diurnas_dom_fes or 0

    @property
    def novedad_horas_extras_nocturnas(self):
        return self.novedad.horas_extras_nocturnas or 0

    @property
    def novedad_horas_extras_nocturnas_dom_fes(self):
        return self.novedad.horas_extras_nocturnas_dom_fes or 0

    @property
    def novedad_horas_recargo_nocturno(self):
        return self.novedad.horas_recargo_nocturno or 0

    @property
    def novedad_horas_recargo_nocturno_dom_fes(self):
        return self.novedad.horas_recargo_nocturno_dom_fes or 0

    @property
    def novedad_horas_recargo_diurno_dom_fes(self):
        return self.novedad.horas_recargo_diurno_dom_fes or 0

    @property
    def novedad_bonificaciones(self):
        return self.novedad.bonificaciones or 0

    def valor_incapacidad(self):
        valor_incapacidad = ((self.novedad_salario / 30) * 0.6666)
        if valor_incapacidad < 43333:
            return 43333 * self.novedad_dias_incapacidad
        else:
            return valor_incapacidad * self.novedad_dias_incapacidad

    def sueldo(self):
        return (self.novedad_salario / 30) * self.novedad_dias_trabajados

    def comisiones_valor(self):
        return self.novedad_comisiones * self.novedad_comisiones_porcentaje

    def auxilio_transporte(self):
        if (self.novedad_salario + self.comisiones_valor()) <= 2600000 and (
                self.sueldo() + self.comisiones_valor()) > 0:
            return 162000 / 30 * self.novedad_dias_trabajados
        else:
            return 0

    def valor_horas_extras_diurnas(self):
        return (self.novedad_salario / 235) * self.novedad_horas_extras_diurnas * 1.25

    def valor_horas_extras_diurnas_dom_fes(self):
        return (self.novedad_salario / 235) * self.novedad_horas_extras_diurnas_dom_fes * 2

    def valor_horas_extras_nocturnas(self):
        return (self.novedad_salario / 235) * self.novedad_horas_extras_nocturnas * 1.75

    def valor_horas_extras_nocturnas_dom_fes(self):
        return (self.novedad_salario / 235) * self.novedad_horas_extras_nocturnas_dom_fes * 2.5

    def valor_horas_recargo_nocturno(self):
        return (self.novedad_salario / 235) * self.novedad_horas_recargo_nocturno * 0.35

    def valor_horas_recargo_nocturno_dom_fes(self):
        return (self.novedad_salario / 235) * self.novedad_horas_recargo_nocturno_dom_fes * 1.1

    def valor_horas_recargo_diurno_dom_fes(self):
        return (self.novedad_salario / 235) * self.novedad_horas_recargo_diurno_dom_fes * 0.75

    def total_horas_extras_recargo(self):
        return (self.valor_horas_extras_diurnas() + self.valor_horas_extras_diurnas_dom_fes() +
                self.valor_horas_extras_nocturnas() + self.valor_horas_extras_nocturnas_dom_fes() +
                self.valor_horas_recargo_nocturno() + self.valor_horas_recargo_nocturno_dom_fes() +
                self.valor_horas_recargo_diurno_dom_fes())

    def ibc(self):
        return (self.sueldo() + self.total_horas_extras_recargo() +
                self.comisiones_valor() + self.novedad_bonificaciones + self.valor_incapacidad())

    def total_devengado(self):
        return self.ibc() + self.auxilio_transporte()

    def __str__(self):
        return f"{self.novedad}"


class Deduccion(models.Model):
    novedad = models.ForeignKey('Novedad', on_delete=models.CASCADE)
    devengado = models.ForeignKey('Devengado', on_delete=models.CASCADE)
    retefuente = models.CharField(max_length=256)

    @property
    def ibc(self):
        return self.devengado.ibc()

    @property
    def novedad_salario(self):
        return self.novedad.salario

    @property
    def novedad_embargos_judiciales(self):
        return self.novedad.embargos_judiciales or 0

    @property
    def novedad_libranzas(self):
        return self.novedad.libranzas or 0

    @property
    def novedad_cooperativas(self):
        return self.novedad.cooperativas or 0

    @property
    def novedad_otros(self):
        return self.novedad.otros or 0

    @property
    def total_devengado(self):
        return self.devengado.total_devengado

    @property
    def salud(self):
        return self.ibc * 0.04

    @property
    def pension(self):
        return self.ibc * 0.04

    @property
    def fsp(self):
        if 5200001 <= self.novedad_salario <= 20800000:
            return float(self.total_devengado()) * 0.01
        elif 20800001 <= self.novedad_salario <= 22100000:
            return float(self.total_devengado()) * 0.012
        elif 22100001 <= self.novedad_salario <= 23400000:
            return float(self.total_devengado()) * 0.014
        elif 23400001 <= self.novedad_salario <= 24700000:
            return float(self.total_devengado()) * 0.016
        elif 24700001 <= self.novedad_salario <= 26000000:
            return float(self.total_devengado()) * 0.018
        elif self.novedad_salario >= 26000001:
            return float(self.total_devengado()) * 0.02
        else:
            return 0

    @property
    def total_deduccion(self):
        return (self.salud + self.pension + self.fsp +
                self.novedad_embargos_judiciales + self.novedad_libranzas +
                self.novedad_cooperativas + self.novedad_otros)

    def __str__(self):
        return f"{self.novedad}"


class Nomina(models.Model):
    novedad = models.ForeignKey('Novedad', on_delete=models.CASCADE)
    devengado = models.ForeignKey('Devengado', on_delete=models.CASCADE)
    deduccion = models.ForeignKey('Deduccion', on_delete=models.CASCADE)

    @property
    def total_devengado(self):
        return self.devengado.total_devengado()

    @property
    def total_deduccion(self):
        return self.deduccion.total_deduccion

    @property
    def total_a_pagar(self):
        return self.total_devengado - self.total_deduccion

    @property
    def ibc(self):
        return float(self.devengado.ibc())

    @property
    def riesgo(self):
        return self.novedad.riesgo

    @property
    def salud(self):
        return self.ibc * 0.085

    @property
    def pension(self):
        return self.ibc * 0.12

    @property
    def arl(self):
        return self.ibc * self.riesgo

    @property
    def sena(self):
        if self.ibc >= 13000000:
            return self.ibc * 0.2
        else:
            return 0

    @property
    def icbf(self):
        if self.ibc >= 13000000:
            return self.ibc * 0.3
        else:
            return 0

    @property
    def caja_compensacion(self):
        return self.ibc * 0.4

    @property
    def cesantias(self):
        return self.ibc * 0.0833

    @property
    def intereses_cesantias(self):
        return self.ibc * 0.01

    @property
    def primas_servicio(self):
        return self.ibc * 0.0833

    @property
    def vacaciones(self):
        return self.ibc * 0.0417

    def __str__(self):
        return f"{self.novedad}"


# Ensure signals are imported
from . import signals
