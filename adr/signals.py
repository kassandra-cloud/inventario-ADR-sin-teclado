from django.db.models.signals import pre_save
from django.dispatch import receiver
from adr.models import (
    HistorialCambios, AllInOne, Notebook, MiniPC, Proyectores,
    BodegaADR, Azotea, AllInOneAdmins
)
from accounts.models import Profile
from adr.middleware import get_current_user


@receiver(pre_save, sender=AllInOne)
@receiver(pre_save, sender=AllInOneAdmins)
@receiver(pre_save, sender=Notebook)
@receiver(pre_save, sender=MiniPC)
@receiver(pre_save, sender=Proyectores)
@receiver(pre_save, sender=BodegaADR)
@receiver(pre_save, sender=Azotea)
def registrar_cambios(sender, instance, **kwargs):
    try:
        # Obtener el estado previo del objeto desde la base de datos
        original_instance = sender.objects.get(pk=instance.pk)

        # Comparar los campos del modelo para detectar cambios
        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(original_instance, field_name, None)
            new_value = getattr(instance, field_name, None)

            # Registrar solo si hay un cambio real
            if old_value != new_value:
                HistorialCambios.objects.create(
                    modelo=sender.__name__,
                    objeto_id=instance.pk,
                    usuario=get_current_user(),
                    campo_modificado=field.verbose_name,
                    valor_anterior=old_value if old_value is not None else "N/A",
                    valor_nuevo=new_value if new_value is not None else "N/A",
                )
    except sender.DoesNotExist:
        # Si el objeto es nuevo, registra "Creación"
        HistorialCambios.objects.create(
            modelo=sender.__name__,
            objeto_id=instance.pk,
            usuario=get_current_user(),
            campo_modificado="Creación",
            valor_anterior="N/A",
            valor_nuevo=str(instance),
        )
