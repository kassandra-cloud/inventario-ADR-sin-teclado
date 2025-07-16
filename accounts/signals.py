from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Profile
from adr.models import HistorialCambios
from .middleware import get_current_user_accounts  # Importar el nuevo middleware

@receiver(pre_save, sender=Profile)
def registrar_cambios_profile(sender, instance, **kwargs):
    print(f"Signal disparada para Profile: {instance}")

    try:
        # Obtener el estado previo del objeto desde la base de datos
        original_instance = sender.objects.get(pk=instance.pk)

        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(original_instance, field_name, None)
            new_value = getattr(instance, field_name, None)

            if old_value != new_value:
                usuario_actual = get_current_user_accounts()  # Usar el middleware de accounts
                print(f"Usuario actual: {usuario_actual}")
                HistorialCambios.objects.create(
                    modelo=sender.__name__,
                    objeto_id=instance.pk,
                    usuario=usuario_actual,
                    campo_modificado=field.verbose_name,
                    valor_anterior=old_value if old_value is not None else "N/A",
                    valor_nuevo=new_value if new_value is not None else "N/A",
                )
                print(f"Historial creado para campo {field_name}")
    except sender.DoesNotExist:
        print(f"Perfil nuevo creado: {instance}")
        usuario_actual = get_current_user_accounts()  # Usar el middleware de accounts
        HistorialCambios.objects.create(
            modelo=sender.__name__,
            objeto_id=instance.pk,
            usuario=usuario_actual,
            campo_modificado="Creación",
            valor_anterior="N/A",
            valor_nuevo=str(instance),
        )
