from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Usuario, Novedad, Devengado, Deduccion, Nomina


# Función para crear una novedad cuando se crea un colaborador
@receiver(post_save, sender=Usuario)
def create_novedad_for_colaborador(sender, instance, created, **kwargs):
    if created and instance.rol == 2:
        # Verificar si el colaborador ya tiene una novedad
        if not Novedad.objects.filter(usuario=instance).exists():
            Novedad.objects.create(usuario=instance)

# Devengado Signals
@receiver(post_save, sender=Novedad)
def create_devengado(sender, instance, created, **kwargs):
    if created:
        Devengado.objects.create(novedad=instance)

@receiver(post_save, sender=Novedad)
def update_devengado_on_novedad_update(sender, instance, created, **kwargs):
    devengado_instance = Devengado.objects.filter(novedad=instance).first()
    if devengado_instance:
        devengado_instance.save()

@receiver(post_delete, sender=Novedad)
def delete_devengado_on_novedad_delete(sender, instance, **kwargs):
    devengado_instance = Devengado.objects.filter(novedad=instance).first()
    if devengado_instance:
        devengado_instance.delete()

# Deduccion Signals
@receiver(post_save, sender=Novedad)
def create_deduccion(sender, instance, created, **kwargs):
    if created:
        devengado_instance = Devengado.objects.filter(novedad=instance).first()
        if devengado_instance:
            Deduccion.objects.create(novedad=instance, devengado=devengado_instance)

@receiver(post_save, sender=Novedad)
def update_deduccion_on_novedad_update(sender, instance, created, **kwargs):
    deduccion_instance = Deduccion.objects.filter(novedad=instance).first()
    if deduccion_instance:
        deduccion_instance.save()

@receiver(post_delete, sender=Novedad)
def delete_deduccion_on_novedad_delete(sender, instance, **kwargs):
    deduccion_instance = Deduccion.objects.filter(novedad=instance).first()
    if deduccion_instance:
        deduccion_instance.delete()

# Nomina Signals
@receiver(post_save, sender=Novedad)
def create_nomina(sender, instance, created, **kwargs):
    if created:
        devengado_instance = Devengado.objects.filter(novedad=instance).first()
        deduccion_instance = Deduccion.objects.filter(novedad=instance).first()
        if devengado_instance and deduccion_instance:
            Nomina.objects.create(novedad=instance, devengado=devengado_instance, deduccion=deduccion_instance)

@receiver(post_save, sender=Novedad)
def update_nomina_on_novedad_update(sender, instance, created, **kwargs):
    # Eliminar la nómina existente para la misma fecha
    Nomina.objects.filter(novedad=instance).delete()

    # Crear la nueva Nómina con la fecha actualizada
    devengado_instance = Devengado.objects.filter(novedad=instance).first()
    deduccion_instance = Deduccion.objects.filter(novedad=instance).first()
    if devengado_instance and deduccion_instance:
        Nomina.objects.create(
            novedad=instance,
            devengado=devengado_instance,
            deduccion=deduccion_instance,
            fecha_nomina=instance.fecha_ultima_actualizacion
        )

@receiver(post_delete, sender=Novedad)
def delete_nomina_on_novedad_delete(sender, instance, **kwargs):
    nomina_instance = Nomina.objects.filter(novedad=instance).first()
    if nomina_instance:
        # Eliminar devengados y deducciones asociados antes de eliminar la nómina
        Devengado.objects.filter(novedad=instance).delete()
        Deduccion.objects.filter(novedad=instance).delete()
        nomina_instance.delete()

@receiver(post_delete, sender=Nomina)
def delete_devengado_deduccion_on_nomina_delete(sender, instance, **kwargs):
    # Eliminar devengados y deducciones asociados a la nómina cuando se elimina la nómina
    Devengado.objects.filter(novedad=instance.novedad).delete()
    Deduccion.objects.filter(novedad=instance.novedad).delete()


@receiver(post_save, sender=Novedad)
def handle_novedad_save(sender, instance, created, **kwargs):
    # Crear o actualizar Devengado
    devengado_instance, _ = Devengado.objects.get_or_create(novedad=instance)

    # Crear o actualizar Deduccion si existe el Devengado
    deduccion_instance, _ = Deduccion.objects.get_or_create(novedad=instance, devengado=devengado_instance)

    # Eliminar la nómina existente para la misma fecha
    Nomina.objects.filter(novedad=instance).delete()

    # Crear la nueva Nómina con la fecha actualizada
    Nomina.objects.create(
        novedad=instance,
        devengado=devengado_instance,
        deduccion=deduccion_instance,
        fecha_nomina=instance.fecha_ultima_actualizacion
    )


@receiver(post_delete, sender=Novedad)
def handle_novedad_delete(sender, instance, **kwargs):
    # Eliminar Devengado, Deduccion y Nómina cuando se elimina una novedad
    Devengado.objects.filter(novedad=instance).delete()
    Deduccion.objects.filter(novedad=instance).delete()
    Nomina.objects.filter(novedad=instance).delete()


"""@receiver(post_delete, sender=Novedad)
def delete_nomina_quincena_on_novedad_delete(sender, instance, **kwargs):
    nomina_quincena_instance = NominaQuincena.objects.filter(novedad=instance).first()
    if nomina_quincena_instance:
        nomina_quincena_instance.delete()"""