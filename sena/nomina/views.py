from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.utils.text import slugify

import pdfkit
from django.db import IntegrityError, transaction
import datetime
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.urls import reverse
from django.contrib import messages
from .models import *
from django.shortcuts import get_object_or_404
from xhtml2pdf import pisa
import io
from urllib.parse import urlencode


# Create your views here.

def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo_login")
        contrasena = request.POST.get("contrasena_login")

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


def index_fake(request):
    return render(request, 'nomina/index.html')


def index(request):
    if request.session.get("logueo", False):
        return render(request, "nomina/index.html")
    else:
        return render(request, 'nomina/login.html')


def colaboradores(request):
    q = Usuario.objects.filter(rol=2)
    cargos = Usuario.CARGOS
    roles = Usuario.ROLES
    contexto = {"data": q, 'CARGOS': cargos, 'ROLES': roles, }
    return render(request, 'nomina/colaborador/colaboradores.html', contexto)


def colaborador_guardar(request):
    if request.method == "POST":
        id = request.POST.get("id")
        nombre = request.POST.get('nombre')
        apellido = request.POST.get("apellido")
        cedula = request.POST.get('cedula')
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        rol = 2
        foto = request.FILES.get("foto")
        cargo = request.POST.get("cargo")

        if id == "":
            try:
                usu = Usuario(
                    nombre=nombre,
                    apellido=apellido,
                    correo=correo,
                    cedula=cedula,
                    contrasena=contrasena,
                    rol=rol,
                    foto=foto,
                    cargo=cargo,
                )
                usu.save()
                messages.success(request, "Guardado correctamente!!")
            except Exception as e:
                messages.error(request, f"Error. {e}")
        return HttpResponseRedirect(reverse("nomina:colaboradores", args=()))
    else:
        messages.warning(request, "No se enviarion datos...")
        return HttpResponseRedirect(reverse("nomina:colaboradores", args=()))


def colaborador_editar(request, id):
    if request.session.get("logueo", False):
        nombre = request.POST.get('nombre_editar')
        apellido = request.POST.get("apellido_editar")
        cedula = request.POST.get('cedula_editar')
        correo = request.POST.get('correo_editar')
        contrasena = request.POST.get('contrasena_editar')
        rol = 2
        foto = request.FILES.get("foto_editar")
        cargo = request.POST.get("cargo_editar")

        try:
            q = Usuario.objects.get(pk=id)
            q.nombre = nombre
            q.apellido = apellido
            q.cedula = cedula
            q.correo = correo
            q.contrasena = contrasena
            q.rol = rol
            if foto:
                q.foto = foto
            q.cargo = cargo
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


def contacto(request):
    return render(request, 'nomina/contacto.html')


def documentacion(request):
    return render(request, 'nomina/documentacion.html')


def liquidaciones(request):
    return render(request, 'nomina/liquidaciones.html')


def nomina(request):
    if request.session.get("logueo", False):
        usuario_id = request.session["logueo"]["id"]
        try:
            usuario = Usuario.objects.get(id=usuario_id)

            if usuario.rol == 2:  # Suponiendo que el rol 2 es para colaboradores
                q = NominaQuincena.objects.filter(nomina__novedad__usuario=usuario)
                q2 = Nomina.objects.filter(novedad__usuario=usuario)
                # Calcular el total a pagar para el usuario logueado
                total_a_pagar_usuario = sum(n.total_a_pagar for n in q2)
            else:
                q = NominaQuincena.objects.all()
                q2 = Nomina.objects.all()
                total_a_pagar_usuario = None

            periodos = q.values('fecha_inicio', 'fecha_fin').distinct()

            contexto = {"data": q, "nomina": q2, "total_a_pagar_usuario": total_a_pagar_usuario, "periodos": periodos }
            return render(request, 'nomina/nomina/nomina.html', contexto)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
            return HttpResponseRedirect(reverse("nomina:login"))
    else:
        messages.warning(request, "Debe iniciar sesión para ver esta página.")
        return HttpResponseRedirect(reverse("nomina:login"))


def nomina_buscar(request):
    pass

def nomina_listar(request, id):
    pass

def nomina_guardar(request):
    if request.method == "POST":
        nomina_ids = request.POST.getlist("nomina[]")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")

        print(f"Nomina IDs: {nomina_ids}")  # Debugging statement
        print(f"Fecha Inicio: {fecha_inicio}")  # Debugging statement
        print(f"Fecha Fin: {fecha_fin}")  # Debugging statement

        if nomina_ids:
            try:
                # Crea la instancia de NominaQuincena sin asignar las nóminas aún
                nomina_quincena = NominaQuincena(
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin
                )
                nomina_quincena.save()

                # Asigna las nóminas seleccionadas a la instancia de NominaQuincena
                nominas_seleccionadas = Nomina.objects.filter(id__in=nomina_ids)
                nomina_quincena.nomina.set(nominas_seleccionadas)
                nomina_quincena.save()

                print(f"Nominas Seleccionadas: {nominas_seleccionadas}")  # Debugging statement

                messages.success(request, "Guardado correctamente!!")
            except Exception as e:
                messages.error(request, f"Error. {e}")
        else:
            messages.error(request, "No se seleccionaron nóminas.")

        return HttpResponseRedirect(reverse("nomina:nomina"))
    else:
        messages.warning(request, "No se enviaron datos...")
        return HttpResponseRedirect(reverse("nomina:nomina"))


def novedades_nomina(request):
    q = Novedad.objects.all()
    usuarios = Usuario.objects.filter(rol=2)
    contexto = {"data": q, 'usuarios': usuarios}
    return render(request, 'nomina/novedad/novedades_nomina.html', contexto)


def novedad_guardar(request):
    if request.method == "POST":
        usuario_id = request.POST.get("usuario")
        usuario = Usuario.objects.get(id=usuario_id)
        salario = request.POST.get("salario")
        clase_salario = request.POST.get("clase_salario")
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
        riesgo = request.POST.get("riesgo")
        fecha_ingreso = request.POST.get("fecha_ingreso")
        fecha_fin_contrato = request.POST.get("fecha_fin_contrato") or None
        tipo_contrato = request.POST.get("tipo_contrato")
        fecha_retiro = request.POST.get("fecha_retiro") or None
        motivo_retiro = request.POST.get("motivo_retiro") or None

        try:
            nov = Novedad(
                usuario=usuario,
                salario=salario,
                clase_salario=clase_salario,
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
                riesgo=riesgo,
                fecha_ingreso=fecha_ingreso,
                fecha_fin_contrato=fecha_fin_contrato,
                tipo_contrato=tipo_contrato,
                fecha_retiro=fecha_retiro,
                motivo_retiro=motivo_retiro,
            )
            nov.save()
            messages.success(request, "Guardado correctamente!!")
        except Exception as e:
            messages.error(request, f"Error. {e}")

        return HttpResponseRedirect(reverse("nomina:novedades_nomina"))
    else:
        messages.warning(request, "No se enviaron datos...")
        return HttpResponseRedirect(reverse("nomina:novedades_nomina"))


def recibos(request):
    return render(request, 'nomina/recibos.html')


def terminos(request):
    return render(request, 'nomina/terminos.html')


# --------------------------------------------


def register(request):
    cargos = Usuario.CARGOS
    roles = Usuario.ROLES
    context = {
        'CARGOS': cargos,
        'ROLES': roles,
    }
    return render(request, 'nomina/register.html', context)


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
        nombre = request.POST.get('nombre')
        apellido = request.POST.get("apellido")
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        rol = request.POST.get("rol")
        foto = request.FILES.get("foto")
        cargo = request.POST.get("cargo")

        if cargo is not None:
            try:
                cargo = int(cargo)  # Convertir el valor de cargo a entero
            except ValueError:
                cargo = None

        if id == "":
            # crear
            try:
                usu = Usuario(
                    nombre=nombre,
                    apellido=apellido,
                    correo=correo,
                    contrasena=contrasena,
                    rol=rol,
                    foto=foto,
                    cargo=cargo,
                )
                usu.save()
                messages.success(request, "Guardado correctamente!!")
            except Exception as e:
                messages.error(request, f"Error. {e}")
        else:
            # actualizar
            try:
                q = Usuario.objects.get(pk=id)
                q.nombre = nombre
                q.apellido = apellido
                q.correo = correo
                q.contrasena = contrasena
                q.rol = rol
                q.foto = foto
                q.cargo = cargo
                q.save()
                messages.success(request, "Actualizado correctamente!!")
            except Exception as e:
                messages.error(request, f"Error. {e}")

        return HttpResponseRedirect(reverse("nomina:index", args=()))

    else:
        messages.warning(request, "No se enviarion datos...")
        return HttpResponseRedirect(reverse("nomina:usuario_formulario", args=()))


def convert_html_to_pdf(source_html):
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(source_html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None


def recibo_view(request, nomina_id):
    nomina = get_object_or_404(Nomina, id=nomina_id)
    nominaquincena = get_object_or_404(NominaQuincena, nomina__id=nomina_id)

    totalh = nomina.novedad.horas_extras_diurnas + nomina.novedad.horas_extras_diurnas_dom_fes + nomina.novedad.horas_extras_nocturnas + nomina.novedad.horas_extras_nocturnas_dom_fes + nomina.novedad.horas_recargo_diurno_dom_fes + nomina.novedad.horas_recargo_nocturno + nomina.novedad.horas_recargo_nocturno_dom_fes

    contexto = {
        "nomina": nomina,
        "quincena": nominaquincena,
        "totalh": totalh
    }

    html_string = render_to_string('nomina/recibo.html', contexto)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="recibo_{nomina_id}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse(f'Error al generar el PDF: {pisa_status.err}')
    return response


def descargar_recibo(request, nomina_id):
    nomina = get_object_or_404(Nomina, id=nomina_id)
    nombre_colaborador = nomina.novedad.usuario.nombre
    apellido_colaborador = nomina.novedad.usuario.apellido
    nominaquincena = get_object_or_404(NominaQuincena, nomina__id=nomina_id)
    fecha_inicio = nominaquincena.fecha_inicio

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


def practica(request):
    nomina = get_object_or_404(Nomina, novedad__usuario__id=2)
    nominaquincena = get_object_or_404(NominaQuincena, nomina__novedad__usuario__id=2)
    contexto = {
        "nomina": nomina,
        "quincena": nominaquincena
    }
    return render(request, 'nomina/recibo.html', contexto)
