from django.contrib import admin
from .models import *
from django.utils.html import mark_safe


# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'correo', 'contrasena', 'rol', 'ver_foto', 'cargo']

    def ver_foto(self, obj):
        try:
            return mark_safe(f"<img src='{obj.foto.url}' style='width:20%;'>")
        except Exception as e:
            return f"Error, el archivo fue eliminado."


class NovedadAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'salario', 'clase_salario', 'dias_incapacidad', 'dias_trabajados',
                    'horas_extras_diurnas', 'horas_extras_diurnas_dom_fes', 'horas_extras_nocturnas',
                    'horas_extras_nocturnas_dom_fes', 'horas_recargo_nocturno', 'horas_recargo_nocturno_dom_fes',
                    'horas_recargo_diurno_dom_fes', 'comisiones', 'comisiones_porcentaje', 'bonificaciones',
                    'embargos_judiciales', 'libranzas', 'cooperativas', 'otros', 'riesgo', 'riesgo_porcentaje',
                    'fecha_ingreso', 'fecha_fin_contrato', 'tipo_contrato', 'fecha_retiro', 'motivo_retiro', 'fecha_novedad']


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
    list_display = ['id', 'novedad', 'total_a_pagar']


class NominaQuincenaAdmin(admin.ModelAdmin):
    list_display = ['id', 'mostrar_nominas', 'fecha_inicio', 'fecha_fin']

    def mostrar_nominas(self, obj):
        nominas_info = [f"{nomina.novedad.usuario.nombre} - Total a pagar: {round(nomina.total_a_pagar, 2)}" for nomina in
                        obj.nomina.all()]
        return " - ".join(nominas_info)

    mostrar_nominas.short_description = 'Nominas'


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Novedad, NovedadAdmin)
admin.site.register(Devengado, DevengadoAdmin)
admin.site.register(Deduccion, DeduccionAdmin)
admin.site.register(Nomina, NominaAdmin)
admin.site.register(NominaQuincena, NominaQuincenaAdmin)
