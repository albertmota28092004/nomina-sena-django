from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Novedad, Devengado, Deduccion, Nomina

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

@receiver(post_save, sender=Novedad)
def create_nomina(sender, instance, created, **kwargs):
    if created:
        devengado_instance = Devengado.objects.filter(novedad=instance).first()
        deduccion_instance = Deduccion.objects.filter(novedad=instance).first()
        if devengado_instance and deduccion_instance :
            Nomina.objects.create(novedad=instance, devengado=devengado_instance, deduccion=deduccion_instance)

@receiver(post_save, sender=Novedad)
def update_nomina_on_novedad_update(sender, instance, created, **kwargs):
    nomina_instance = Nomina.objects.filter(novedad=instance).first()
    if nomina_instance:
        nomina_instance.save()

@receiver(post_delete, sender=Novedad)
def delete_nomina_on_novedad_delete(sender, instance, **kwargs):
    nomina_instance = Nomina.objects.filter(novedad=instance).first()
    if nomina_instance:
        nomina_instance.delete()


