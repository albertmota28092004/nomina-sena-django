from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.utils.dateparse import parse_date

from django.core.mail import BadHeaderError, EmailMessage
from django.conf import settings
import datetime
import pdfkit
from django.db import IntegrityError, transaction
import datetime
import openpyxl
import xlwings as xw
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, Max
from django.urls import reverse
from django.contrib import messages
from .models import *
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
import io
from django.db.models.functions import TruncMonth
from django.db.models import Count
from urllib.parse import urlencode
from django.utils import timezone


# Create your views here.

def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo_login")
        contrasena = request.POST.get("contrasena_login")
        remember_me = request.POST.get("remember_me", False)

        try:
            q = Usuario.objects.get(correo=correo, contrasena=contrasena)
            messages.success(request, f"Bienvenido sr(a) {q.nombre}!!")
            datos = {
                "rol": q.rol,
                "nombre_rol": q.get_rol_display(),
                "nombre": f"{q.nombre} {q.apellido}",
                "foto": q.foto.url if q.foto else "/media/fotos/default.png",
                "id": q.id
            }
            request.session["logueo"] = datos

            # Manejo del "Recordar usuario"
            if remember_me:
                request.session.set_expiry(1209600)  # 2 semanas
            else:
                request.session.set_expiry(0)  # Cerrar la sesión al cerrar el navegador

            return HttpResponseRedirect(reverse("nomina:index"))
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario o contraseña no válidos...")
            return render(request, "nomina/login.html")
    else:
        if request.session.get("logueo", False):
            return HttpResponseRedirect(reverse("nomina:index"))
        else:
            return render(request, "nomina/login.html")


def logout(request):
    try:
        del request.session["logueo"]
        messages.success(request, "Cesión cerrada correctamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return HttpResponseRedirect(reverse("nomina:login"))


def landing_page(request):
    if request.session.get("logueo", False):
        return render(request, "nomina/index.html")
    else:
        return render(request, 'nomina/landing-page.html')


def index(request):
    if request.session.get("logueo", False):
        return render(request, "nomina/index.html")
    else:
        return render(request, 'nomina/login.html')


def registrarse(request):
    cargos = Usuario.CARGOS
    roles = Usuario.ROLES
    context = {
        'CARGOS': cargos,
        'ROLES': roles,
    }
    return render(request, 'nomina/registrarse.html', context)


def crear_admin(request):
    pass


def convert_html_to_pdf(source_html):
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(source_html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None


def recibo_view(request, nomina_id):
    nomina = get_object_or_404(Nomina, id=nomina_id)

    totalh = nomina.novedad.horas_extras_diurnas + nomina.novedad.horas_extras_diurnas_dom_fes + nomina.novedad.horas_extras_nocturnas + nomina.novedad.horas_extras_nocturnas_dom_fes + nomina.novedad.horas_recargo_diurno_dom_fes + nomina.novedad.horas_recargo_nocturno + nomina.novedad.horas_recargo_nocturno_dom_fes

    contexto = {
        "nomina": nomina,
        "totalh": totalh
    }

    html_string = render_to_string('nomina/recibo.html', contexto)
    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'] = f'inline; filename="Recibo_{nomina.novedad.usuario}_{nomina.novedad.fecha_fin}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}')
    return response


def descargar_recibo(request, nomina_id):
    nomina = get_object_or_404(Nomina, id=nomina_id)
    nombre_colaborador = nomina.novedad.usuario.nombre
    apellido_colaborador = nomina.novedad.usuario.apellido
    fecha_inicio = nomina.fecha_inicio

    contexto = {
        "nomina": nomina,
    }
    html_string = render_to_string('nomina/recibo.html', contexto)
    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'] = f'inline; filename="recibo_{slugify(nombre_colaborador)}{slugify(apellido_colaborador)}_{fecha_inicio}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}')
    return response


def parafiscales(request, id):
    if request.session.get("logueo", False):
        nomina = Nomina.objects.get(pk=id)
        print(nomina)
        contexto = {'data': nomina}
        return render(request, 'nomina/parafiscales.html', contexto)


def provisiones(request, id):
    if request.session.get("logueo", False):
        nomina = Nomina.objects.get(pk=id)
        contexto = {'data': nomina}
        return render(request, 'nomina/provisiones.html', contexto)


def liquidacion(request, id):
    if request.session.get("logueo", False):
        usuario = Usuario.objects.get(pk=id)
        nomina = Nomina.objects.filter(novedad__usuario=usuario)
        novedad = Novedad.objects.filter(usuario=usuario).exists()

        if not novedad:
            messages.warning(request, 'Este colaborador necesita tener una nómina para poder ser liquidado.')
            return redirect('nomina:colaboradores')

        contexto = {'usuario': usuario, 'nomina': nomina}
        return render(request, 'nomina/liquidacion/liquidacion.html', contexto)


def liquidacion_archivo(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    nomina = Nomina.objects.get(novedad__usuario=usuario)

    novedades = nomina.novedad_set.all()
    dias_trabajados = sum(novedad.dias_trabajados for novedad in novedades)
    cesantias = (nomina.novedad.salario * dias_trabajados) / 360
    intereses_cesantias = (cesantias * 0.12 * dias_trabajados) / 360
    prima_servicio = (nomina.novedad.salario * dias_trabajados) / 360
    vacaciones = (nomina.novedad.salario * dias_trabajados) / 720
    total_liquidacion = cesantias + intereses_cesantias + prima_servicio + vacaciones
    neto_pagado = total_liquidacion + nomina.total_a_pagar

    contexto = {
        'usuario': usuario,
        'nomina': nomina,
        'dias_trabajados': dias_trabajados,
        "cesantias": cesantias,
        "intereses_cesantias": intereses_cesantias,
        "prima_servicio": prima_servicio,
        "vacaciones": vacaciones,
        "total_liquidacion": total_liquidacion,
        "neto_pagado": neto_pagado,
    }

    return render(request, 'nomina/liquidacion/liquidacion-archivo.html', contexto)


def liquidacion_view(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    # Obtener todas las nóminas relacionadas con el usuario, ordenadas por la fecha fin de la novedad
    nominas = Nomina.objects.filter(novedad__usuario=usuario).order_by('-novedad__fecha_fin')

    if nominas.exists():
        nomina = nominas.first()  # Obtener la nómina más reciente
    else:
        return HttpResponse('No se encontraron nóminas para el usuario.', status=404)

    # Obtener todas las novedades relacionadas con el usuario
    novedades = Novedad.objects.filter(usuario=usuario)
    dias_trabajados = sum(novedad.dias_trabajados for novedad in novedades)

    # Calcular las cesantías y otros valores
    salario = nomina.novedad.salario
    cesantias = (salario * dias_trabajados) / 360
    intereses_cesantias = (cesantias * 0.12 * dias_trabajados) / 360
    prima_servicio = (salario * dias_trabajados) / 360
    vacaciones = (salario * dias_trabajados) / 720
    total_liquidacion = cesantias + intereses_cesantias + prima_servicio + vacaciones
    neto_pagado = total_liquidacion + nomina.total_a_pagar

    contexto = {
        'usuario': usuario,
        'nomina': nomina,
        'dias_trabajados': dias_trabajados,
        "cesantias": cesantias,
        "intereses_cesantias": intereses_cesantias,
        "prima_servicio": prima_servicio,
        "vacaciones": vacaciones,
        "total_liquidacion": total_liquidacion,
        "neto_pagado": neto_pagado,
    }

    html_string = render_to_string('nomina/liquidacion/liquidacion-archivo.html', contexto)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Liquidacion_{usuario.nombre}_{usuario.apellido}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}')
    return response


def liquidar_colaborador(request, id):
    usuario = Usuario.objects.get(pk=id)
    nominas = Nomina.objects.filter(novedad__usuario=usuario).order_by('-novedad__fecha_fin')

    if nominas.exists():
        nomina = nominas.first()  # Obtener la nómina más reciente
    else:
        return HttpResponse('No se encontraron nóminas para el usuario.', status=404)

    salario = nomina.novedad.salario
    dias_incapacidad = nomina.novedad.dias_incapacidad or 0
    dias_trabajados = nomina.novedad.dias_trabajados
    horas_extras_diurnas = nomina.novedad.horas_extras_diurnas or 0
    horas_extras_diurnas_dom_fes = nomina.novedad.horas_extras_diurnas_dom_fes or 0
    horas_extras_nocturnas = nomina.novedad.horas_extras_nocturnas or 0
    horas_extras_nocturnas_dom_fes = nomina.novedad.horas_extras_nocturnas_dom_fes or 0
    horas_recargo_nocturno = nomina.novedad.horas_recargo_nocturno or 0
    horas_recargo_nocturno_dom_fes = nomina.novedad.horas_recargo_nocturno_dom_fes or 0
    horas_recargo_diurno_dom_fes = nomina.novedad.horas_recargo_diurno_dom_fes or 0
    comisiones = nomina.novedad.comisiones or 0
    comisiones_porcentaje = nomina.novedad.comisiones_porcentaje or None
    bonificaciones = nomina.novedad.bonificaciones or 0
    embargos_judiciales = nomina.novedad.embargos_judiciales or 0
    libranzas = nomina.novedad.libranzas or 0
    cooperativas = nomina.novedad.cooperativas or 0
    otros = nomina.novedad.otros or 0
    fecha_inicio = nomina.novedad.fecha_inicio
    fecha_fin = nomina.novedad.fecha_fin

    try:
        nov = Novedad(
            usuario=usuario,
            salario=salario,
            dias_incapacidad=dias_incapacidad,
            dias_trabajados=dias_trabajados,
            horas_extras_diurnas=horas_extras_diurnas,
            horas_extras_diurnas_dom_fes=horas_extras_diurnas_dom_fes,
            horas_extras_nocturnas=horas_extras_nocturnas,
            horas_extras_nocturnas_dom_fes=horas_extras_nocturnas_dom_fes,
            horas_recargo_nocturno=horas_recargo_nocturno,
            horas_recargo_nocturno_dom_fes=horas_recargo_nocturno_dom_fes,
            horas_recargo_diurno_dom_fes=horas_recargo_diurno_dom_fes,
            comisiones=comisiones,
            comisiones_porcentaje=comisiones_porcentaje,
            bonificaciones=bonificaciones,
            embargos_judiciales=embargos_judiciales,
            libranzas=libranzas,
            cooperativas=cooperativas,
            otros=otros,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        nov.save()
        messages.success(request, "Colaborador liquidado correctamente!!")
    except Exception as e:
        messages.error(request, f"Error. {e}")

    try:
        q = Usuario.objects.get(pk=id)
        q.nombre = usuario.nombre
        q.apellido = usuario.apellido
        q.correo = usuario.correo
        q.contrasena = usuario.contrasena
        q.rol = usuario.rol
        q.foto = usuario.foto
        q.cargo = usuario.cargo
        q.riesgo = usuario.riesgo
        q.fecha_fin_contrato = timezone.now()
        q.tipo_contrato = usuario.tipo_contrato
        q.activo = False
        q.fecha_retiro = timezone.now()
        q.motivo_retiro = 'Retiro voluntario'
        q.save()
        messages.success(request, "Actualizado correctamente!!")
    except Exception as e:
        messages.error(request, f"Error. {e}")

    return HttpResponseRedirect(reverse("nomina:colaboradores"))


def descargar_liquidacion(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    nombre_colaborador = usuario.nombre
    apellido_colaborador = usuario.apellido

    contexto = {
        "usuario": usuario,
        # Añadir aquí cualquier otro dato necesario para la liquidación
    }
    html_string = render_to_string('nomina/liquidacion/liquidacion-archivo.html', contexto)
    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'] = f'attachment; filename="liquidacion_{slugify(nombre_colaborador)}_{slugify(apellido_colaborador)}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}')
    return response


# -------------------- Modelos --------------------------

def colaboradores(request):
    if request.session.get("logueo", False):
        q = Usuario.objects.filter(rol=2).filter(activo=True)
        q2 = Usuario.objects.filter(rol=2).filter(activo=False)
        book = openpyxl.load_workbook('nomina/excel_files/excel_copia.xlsm')
        sheet = book['EMPLEADOS']
        valor = sheet['B3']
        cargos = Usuario.CARGOS
        roles = Usuario.ROLES
        clase_contrato = Usuario.CLASE_CONTRATO
        contexto = {"data": q, 'retirados': q2, 'CARGOS': cargos, 'CLASE_CONTRATO': clase_contrato, 'ROLES': roles,
                    'valor': valor}
        return render(request, 'nomina/colaborador/colaboradores.html', contexto)
    else:
        messages.warning(request, "Debe iniciar sesión para ver esta página.")
        return HttpResponseRedirect(reverse("nomina:login"))


def prueba(request):
    if request.session.get("logueo", False):
        # Abre el archivo Excel con xlwings
        wb = xw.Book('nomina/excel_files/excel_copia.xlsm')
        sheet_empleados = wb.sheets['EMPLEADOS']
        sheet_datos = wb.sheets['DATOS']

        # Lee los datos de empleados (nombre, cargo) de la hoja EMPLEADOS
        empleados = []
        for row in range(3, 13):  # Filas de 3 a 12
            cedula = sheet_empleados[f'A{row}'].value
            nombre = sheet_empleados[f'B{row}'].value
            cargo = sheet_empleados[f'C{row}'].value

            # Busca el salario correspondiente al cargo en la hoja DATOS
            salarios_rango = sheet_datos.range('B35:C74').value  # Lee todos los cargos y salarios
            salario = 0
            for cargo_datos, salario_datos in salarios_rango:
                if cargo == cargo_datos:
                    salario = salario_datos
                    break

            empleados.append({
                'cedula': cedula,
                'nombre': nombre,
                'cargo': cargo,
                'salario': salario,
            })

        # Asegúrate de actualizar las fórmulas y cálculos
        wb.app.calculate()

        # Cierra el libro sin guardar (opcional si no deseas guardar cambios)
        wb.close()

        contexto = {'empleados': empleados}
        return render(request, 'nomina/prueba.html', contexto)
    else:
        messages.warning(request, "Debe iniciar sesión para ver esta página.")
        return redirect('nomina:login')

def colaborador_guardar(request):
    if request.method == "POST":
        id = request.POST.get("id")
        nombre = request.POST.get('nombre')
        apellido = request.POST.get("apellido")
        cedula = request.POST.get('cedula')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')
        rol = 2
        foto = request.FILES.get("foto")
        cargo = request.POST.get("cargo")
        riesgo = request.POST.get("riesgo")
        tipo_contrato = request.POST.get("tipo_contrato") or None
        fecha_fin_contrato = request.POST.get("fecha_fin_contrato") or None
        fecha_retiro = request.POST.get("fecha_retiro") or None
        motivo_retiro = request.POST.get("motivo_retiro") or None
        if contrasena == confirmar_contrasena:
            contrasena_oficial = contrasena

        if id == "":
            try:
                usu = Usuario(
                    nombre=nombre,
                    apellido=apellido,
                    correo=correo,
                    cedula=cedula,
                    contrasena=contrasena_oficial,
                    rol=rol,
                    foto=foto,
                    cargo=cargo,
                    riesgo=riesgo,
                    tipo_contrato=tipo_contrato,
                    fecha_fin_contrato=fecha_fin_contrato,
                    fecha_retiro=fecha_retiro,
                    motivo_retiro=motivo_retiro,
                )
                usu.save()
                destinatario = usu.correo

                mensaje = f"""
                    <h1 style='color:blue;'>¡Ya eres parte de nuestra familia <strong>PRESS</strong>!</h1>
                    <p>Tu registro fue exitoso. Ya puedes acceder a todas nuestras funciones ingresando con tu correo electrónico y esta contraseña: {usu.contrasena}. Puedes cambiarla cuando desees.</p>
                    <a href='https://senapress.pythonanywhere.com'>Ingresa desde este link</a>
                """

                try:
                    msg = EmailMessage("PRESS", mensaje, settings.EMAIL_HOST_USER, [destinatario])
                    msg.content_subtype = "html"  # Habilitar html
                    msg.send()
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
                except Exception as e:
                    return HttpResponse(f"Error: {e}")
                messages.success(request, "Guardado correctamente!!")
            except Exception as e:
                messages.error(request, f"Error. {e}")
        return HttpResponseRedirect(reverse("nomina:colaboradores", args=()))
    else:
        messages.warning(request, "No se enviarion datos...")
        return HttpResponseRedirect(reverse("nomina:colaboradores", args=()))


def colaborador_editar(request, id):
    if request.session.get("logueo", False):
        usuario = Usuario.objects.get(pk=id)
        nombre = request.POST.get('nombre_editar')
        apellido = request.POST.get("apellido_editar")
        cedula = request.POST.get('cedula_editar')
        correo = request.POST.get('correo_editar')
        contrasena = request.POST.get('contrasena_editar')
        confirmar_contrasena = request.POST.get('confirmar_contrasena_editar')
        rol = 2
        foto = request.FILES.get("foto_editar")
        cargo = request.POST.get("cargo_editar")
        riesgo = request.POST.get("riesgo_editar") or usuario.riesgo
        tipo_contrato = request.POST.get("tipo_contrato_editar") or None
        fecha_fin_contrato = request.POST.get("fecha_fin_contrato_editar") or None
        fecha_retiro = request.POST.get("fecha_retiro_editar") or None
        motivo_retiro = request.POST.get("motivo_retiro_editar") or None

        try:
            q = Usuario.objects.get(pk=id)
            q.nombre = nombre
            q.apellido = apellido
            q.cedula = cedula
            q.correo = correo
            if contrasena == confirmar_contrasena:
                q.contrasena = contrasena
            else:
                messages.error(request, f"Las contraseñas no coinciden...")
            q.rol = rol
            if foto:
                q.foto = foto
            q.cargo = cargo
            q.riesgo = riesgo
            q.tipo_contrato = tipo_contrato
            q.fecha_fin_contrato = fecha_fin_contrato
            q.fecha_retiro = fecha_retiro
            q.motivo_retiro = motivo_retiro
            q.save()
            messages.success(request, "Actualizado correctamente!!")
        except Exception as e:
            messages.error(request, f"Error. {e}")

        return redirect('nomina:colaboradores')


def colaborador_eliminar(request, id):
    try:
        q = Usuario.objects.get(pk=id)
        q.delete()
        messages.success(request, "Eliminado correctamente!!")
    except Exception as e:
        messages.error(request, f"Error. {e}")
    return HttpResponseRedirect(reverse("nomina:colaboradores", args=()))


def nomina(request):
    if request.session.get("logueo", False):
        usuario_id = request.session["logueo"]["id"]
        try:
            usuario = Usuario.objects.get(id=usuario_id)

            if usuario.rol == 2:  # Suponiendo que el rol 2 es para colaboradores
                novedades = Novedad.objects.filter(usuario=usuario)
                total_a_pagar_usuario = sum(n.total_a_pagar for n in Nomina.objects.filter(novedad__usuario=usuario))
            else:
                novedades = Novedad.objects.all()
                total_a_pagar_usuario = None

            # Agrupar nóminas por periodo
            nominas_por_periodo = {}
            for novedad in novedades:
                periodo = (novedad.fecha_inicio, novedad.fecha_fin)
                if periodo not in nominas_por_periodo:
                    nominas_por_periodo[periodo] = []
                nominas_por_periodo[periodo].append(novedad.usuario)

            contexto = {
                "nominas_por_periodo": nominas_por_periodo,
                "total_a_pagar_usuario": total_a_pagar_usuario
            }
            return render(request, 'nomina/nomina/nomina.html', contexto)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
            return HttpResponseRedirect(reverse("nomina:login"))
    else:
        messages.warning(request, "Debe iniciar sesión para ver esta página.")
        return HttpResponseRedirect(reverse("nomina:login"))


def nomina_listar(request, fecha_inicio, fecha_fin):
    if request.session.get("logueo", False):
        usuario_id = request.session["logueo"]["id"]
        usuario = Usuario.objects.get(id=usuario_id)

        if usuario.rol == 1:
            try:
                nominas = Nomina.objects.filter(novedad__fecha_inicio=fecha_inicio, novedad__fecha_fin=fecha_fin)

                contexto = {
                    "nominas": nominas
                }
                return render(request, 'nomina/nomina/nomina-listar.html', contexto)
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario no encontrado")
                return HttpResponseRedirect(reverse("nomina:nomina_listar"))

        if usuario.rol == 2:
            try:
                nominas = Nomina.objects.filter(novedad__usuario=usuario, novedad__fecha_inicio=fecha_inicio,
                                                novedad__fecha_fin=fecha_fin)

                contexto = {
                    "nominas": nominas
                }
                return render(request, 'nomina/nomina/nomina-listar.html', contexto)
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario no encontrado")
                return HttpResponseRedirect(reverse("nomina:nomina_listar"))
    else:
        messages.warning(request, "Debe iniciar sesión para ver esta página.")
        return HttpResponseRedirect(reverse("nomina:login"))


def novedades_nomina(request):
    if request.session.get("logueo", False):
        novedades = Novedad.objects.annotate(month=TruncMonth('fecha_fin')).values('month').annotate(
            c=Count('id')).order_by('-month')
        novedades_por_mes = {}

        for novedad in novedades:
            mes = novedad['month']
            novedades_mes = Novedad.objects.filter(fecha_fin__month=mes.month, fecha_fin__year=mes.year)
            novedades_por_mes[mes] = novedades_mes
        usuarios = Usuario.objects.filter(rol=2).filter(activo=True)

        fechas_ocupadas_inicio = list(Novedad.objects.values_list('fecha_inicio', flat=True))
        fechas_ocupadas_fin = list(Novedad.objects.values_list('fecha_fin', flat=True))

        contexto = {
            "novedades_por_mes": novedades_por_mes,
            'usuarios': usuarios,
            'fechas_ocupadas_inicio': fechas_ocupadas_inicio,
            'fechas_ocupadas_fin': fechas_ocupadas_fin,
        }
        return render(request, 'nomina/novedad/novedades_nomina.html', contexto)
    else:
        messages.warning(request, "Debe iniciar sesión para ver esta página.")
        return HttpResponseRedirect(reverse("nomina:login"))


def novedad_guardar(request):
    if request.method == "POST":
        usuario_id = request.POST.get("usuario")
        usuario = Usuario.objects.get(id=usuario_id)
        salario = request.POST.get("salario")
        dias_incapacidad = request.POST.get("dias_incapacidad") or 0
        dias_trabajados = request.POST.get("dias_trabajados")
        horas_extras_diurnas = request.POST.get("horas_extras_diurnas") or 0
        horas_extras_diurnas_dom_fes = request.POST.get("horas_extras_diurnas_dom_fes") or 0
        horas_extras_nocturnas = request.POST.get("horas_extras_nocturnas") or 0
        horas_extras_nocturnas_dom_fes = request.POST.get("horas_extras_nocturnas_dom_fes") or 0
        horas_recargo_nocturno = request.POST.get("horas_recargo_nocturno") or 0
        horas_recargo_nocturno_dom_fes = request.POST.get("horas_recargo_nocturno_dom_fes") or 0
        horas_recargo_diurno_dom_fes = request.POST.get("horas_recargo_diurno_dom_fes") or 0
        comisiones = request.POST.get("comisiones") or 0
        comisiones_porcentaje = request.POST.get("comisiones_porcentaje") or None
        bonificaciones = request.POST.get("bonificaciones") or 0
        embargos_judiciales = request.POST.get("embargos_judiciales") or 0
        libranzas = request.POST.get("libranzas") or 0
        cooperativas = request.POST.get("libranzas") or 0
        otros = request.POST.get("otros") or 0
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")

        try:
            nov = Novedad(
                usuario=usuario,
                salario=salario,
                dias_incapacidad=dias_incapacidad,
                dias_trabajados=dias_trabajados,
                horas_extras_diurnas=horas_extras_diurnas,
                horas_extras_diurnas_dom_fes=horas_extras_diurnas_dom_fes,
                horas_extras_nocturnas=horas_extras_nocturnas,
                horas_extras_nocturnas_dom_fes=horas_extras_nocturnas_dom_fes,
                horas_recargo_nocturno=horas_recargo_nocturno,
                horas_recargo_nocturno_dom_fes=horas_recargo_nocturno_dom_fes,
                horas_recargo_diurno_dom_fes=horas_recargo_diurno_dom_fes,
                comisiones=comisiones,
                comisiones_porcentaje=comisiones_porcentaje,
                bonificaciones=bonificaciones,
                embargos_judiciales=embargos_judiciales,
                libranzas=libranzas,
                cooperativas=cooperativas,
                otros=otros,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            nov.save()
            messages.success(request, "Guardado correctamente!!")
        except Exception as e:
            messages.error(request, f"Error. {e}")

        return HttpResponseRedirect(reverse("nomina:novedades_nomina"))
    else:
        messages.warning(request, "No se enviaron datos...")
        return HttpResponseRedirect(reverse("nomina:novedades_nomina"))


def novedad_editar(request, id):
    if request.session.get("logueo", False):
        novedad = get_object_or_404(Novedad, id=id)
        usuario_id = request.POST.get("usuario_editar")
        usuario = Usuario.objects.get(id=usuario_id)
        salario = request.POST.get("salario_editar")
        dias_incapacidad = request.POST.get("dias_incapacidad_editar") or 0
        dias_trabajados = request.POST.get("dias_trabajados_editar")
        horas_extras_diurnas = request.POST.get("horas_extras_diurnas_editar") or 0
        horas_extras_diurnas_dom_fes = request.POST.get("horas_extras_diurnas_dom_fes_editar") or 0
        horas_extras_nocturnas = request.POST.get("horas_extras_nocturnas_editar") or 0
        horas_extras_nocturnas_dom_fes = request.POST.get("horas_extras_nocturnas_dom_fes_editar") or 0
        horas_recargo_nocturno = request.POST.get("horas_recargo_nocturno_editar") or 0
        horas_recargo_nocturno_dom_fes = request.POST.get("horas_recargo_nocturno_dom_fes_editar") or 0
        horas_recargo_diurno_dom_fes = request.POST.get("horas_recargo_diurno_dom_fes_editar") or 0
        comisiones = request.POST.get("comisiones_editar") or 0
        comisiones_porcentaje = request.POST.get("comisiones_porcentaje_editar") or None
        bonificaciones = request.POST.get("bonificaciones_editar") or 0
        embargos_judiciales = request.POST.get("embargos_judiciales_editar") or 0
        libranzas = request.POST.get("libranzas_editar") or 0
        cooperativas = request.POST.get("libranzas_editar") or 0
        otros = request.POST.get("otros_editar") or 0
        fecha_inicio = request.POST.get("fecha_inicio_editar") or novedad.fecha_inicio
        fecha_fin = request.POST.get("fecha_fin_editar") or novedad.fecha_fin

        try:
            q = Novedad.objects.get(pk=id)
            q.usuario = usuario
            q.salario = salario
            q.dias_incapacidad = dias_incapacidad
            q.dias_trabajados = dias_trabajados
            q.horas_extras_diurnas = horas_extras_diurnas
            q.horas_extras_diurnas_dom_fes = horas_extras_diurnas_dom_fes
            q.horas_extras_nocturnas = horas_extras_nocturnas
            q.horas_extras_nocturnas_dom_fes = horas_extras_nocturnas_dom_fes
            q.horas_recargo_nocturno = horas_recargo_nocturno
            q.horas_recargo_nocturno_dom_fes = horas_recargo_nocturno_dom_fes
            q.horas_recargo_diurno_dom_fes = horas_recargo_diurno_dom_fes
            q.comisiones = comisiones
            q.comisiones_porcentaje = comisiones_porcentaje
            q.bonificaciones = bonificaciones
            q.embargos_judiciales = embargos_judiciales
            q.libranzas = libranzas
            q.cooperativas = cooperativas
            q.otros = otros
            q.fecha_inicio = fecha_inicio
            q.fecha_fin = fecha_fin
            q.save()
            messages.success(request, "Actualizado correctamente!!")
        except Exception as e:
            messages.error(request, f"Error. {e}")

        return redirect('nomina:novedades_nomina')


def novedad_eliminar(request, id):
    try:
        q = Novedad.objects.get(pk=id)
        q.delete()
        messages.success(request, "Eliminado correctamente!!")
    except Exception as e:
        messages.error(request, f"Error. {e}")
    return HttpResponseRedirect(reverse("nomina:novedades_nomina", args=()))


def usuario_listar(request):
    return render(request, 'nomina/usuario/usuario-listar.html')


def usuario_formulario(request):
    return render(request, 'nomina/usuario/usuario-formulario.html')


def usuario_guardar_imagen(f, nuevo_nombre):
    with open(f"uploads/fotos/{nuevo_nombre}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def usuario_guardar(request):
    if request.method == "POST":
        id = request.POST.get("id")
        cedula = request.POST.get("cedula")
        nombre = request.POST.get('nombre')
        apellido = request.POST.get("apellido")
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        rol = 1
        foto = request.FILES.get("foto")
        cargo = request.POST.get("cargo") or None
        riesgo = request.POST.get("riesgo") or 0
        fecha_fin_contrato = request.POST.get("fecha_fin_contrato") or None
        tipo_contrato = request.POST.get("tipo_contrato") or None
        fecha_retiro = request.POST.get("fecha_retiro") or None
        motivo_retiro = request.POST.get("motivo_retiro") or None

        if cargo is not None:
            try:
                cargo = int(cargo)  # Convertir el valor de cargo a entero
            except ValueError:
                cargo = None

        if id == "":
            # crear
            try:
                usu = Usuario(
                    cedula=cedula,
                    nombre=nombre,
                    apellido=apellido,
                    correo=correo,
                    contrasena=contrasena,
                    rol=rol,
                    foto=foto,
                    cargo=cargo,
                    riesgo=riesgo,
                    fecha_fin_contrato=fecha_fin_contrato,
                    tipo_contrato=tipo_contrato,
                    fecha_retiro=fecha_retiro,
                    motivo_retiro=motivo_retiro,
                )
                usu.save()
                messages.success(request, "Guardado correctamente!!")
                try:
                    destinatario = usu.correo

                    mensaje = f"""
                        <h1 style='color:blue;'>¡Ya eres parte de nuestra familia <strong>PRESS</strong>!</h1>
                        <p>Tu registro fue exitoso. Ya puedes acceder a todas nuestras funciones ingresando con tu correo electrónico y esta contraseña: {usu.contrasena}. Puedes cambiarla cuando desees.</p>
                        <a href='https://senapress.pythonanywhere.com'>Ingresa desde este link</a>
                    """

                    try:
                        msg = EmailMessage("PRESS", mensaje, settings.EMAIL_HOST_USER, [destinatario])
                        msg.content_subtype = "html"  # Habilitar html
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    except Exception as e:
                        return HttpResponse(f"Error: {e}")

                except Exception as e:
                    print(f"{e}")

            except Exception as e:
                messages.error(request, f"Error. {e}")
        else:
            # actualizar
            try:
                q = Usuario.objects.get(pk=id)
                q.cedula = cedula
                q.nombre = nombre
                q.apellido = apellido
                q.correo = correo
                q.contrasena = contrasena
                q.rol = rol
                q.foto = foto
                q.cargo = cargo
                q.riesgo = riesgo
                q.fecha_fin_contrato = fecha_fin_contrato
                q.tipo_contrato = tipo_contrato
                q.fecha_retiro = fecha_retiro
                q.motivo_retiro = motivo_retiro
                q.save()
                messages.success(request, "Actualizado correctamente!!")
            except Exception as e:
                messages.error(request, f"Error. {e}")

        return HttpResponseRedirect(reverse("nomina:index", args=()))

    else:
        messages.warning(request, "No se enviarion datos...")
        return HttpResponseRedirect(reverse("nomina:usuario_formulario", args=()))
