from django.contrib import admin
from .models import *
from django.utils.html import mark_safe


# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'cedula', 'nombre', 'apellido', 'correo', 'contrasena', 'rol', 'ver_foto', 'cargo', 'salario', 'fecha_ingreso',
                    'riesgo',
                    'tipo_contrato', 'fecha_fin_contrato', 'activo', 'fecha_retiro', 'motivo_retiro']

    def ver_foto(self, obj):
        try:
            return mark_safe(f"<img src='{obj.foto.url}' style='width:20%;'>")
        except Exception as e:
            return f"Error, el archivo fue eliminado."


class NovedadAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'dias_incapacidad', 'dias_trabajados',
                    'horas_extras_diurnas', 'horas_extras_diurnas_dom_fes', 'horas_extras_nocturnas',
                    'horas_extras_nocturnas_dom_fes', 'horas_recargo_nocturno', 'horas_recargo_nocturno_dom_fes',
                    'horas_recargo_diurno_dom_fes', 'comisiones', 'comisiones_porcentaje', 'bonificaciones',
                    'embargos_judiciales', 'libranzas', 'cooperativas', 'otros',
                    'fecha_ultima_actualizacion']


class DevengadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'novedad',
                    'valor_incapacidad', 'sueldo',
                    'valor_horas_extras_diurnas', 'valor_horas_extras_diurnas_dom_fes',
                    'valor_horas_extras_nocturnas', 'valor_horas_extras_nocturnas_dom_fes',
                    'valor_horas_recargo_nocturno', 'valor_horas_recargo_nocturno_dom_fes',
                    'valor_horas_recargo_diurno_dom_fes', 'total_horas_extras_recargo', 'comisiones_valor',
                    'novedad_bonificaciones', 'total_devengado']


class DeduccionAdmin(admin.ModelAdmin):
    list_display = ['id', 'novedad', 'salud', 'pension', 'fsp', 'retefuente', 'novedad_embargos_judiciales',
                    'novedad_libranzas', 'novedad_cooperativas', 'novedad_otros', 'total_deduccion']


class NominaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_nomina', 'novedad', 'salud', 'pension', 'arl', 'sena', 'icbf',
                    'caja_compensacion', "cesantias", "intereses_cesantias", "primas_servicio", "vacaciones",
                    'total_a_pagar']


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Novedad, NovedadAdmin)
admin.site.register(Devengado, DevengadoAdmin)
admin.site.register(Deduccion, DeduccionAdmin)
admin.site.register(Nomina, NominaAdmin)
