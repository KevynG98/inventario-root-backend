from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models.perfilModel import Perfil
from .models.inventarioProductoModel import InventarioProducto
import cloudinary.uploader

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(pre_save, sender=InventarioProducto)
def eliminar_imagen_antigua_al_actualizar(sender, instance, **kwargs):
    """
    Elimina la imagen antigua de Cloudinary cuando se actualiza con una nueva
    o se limpia el campo.
    """
    if not instance.pk:
        return

    try:
        old_instance = InventarioProducto.objects.get(pk=instance.pk)
    except InventarioProducto.DoesNotExist:
        return

    old_file = old_instance.imagen
    new_file = instance.imagen

    # Si había imagen y (se cambió por otra o se eliminó)
    if old_file and old_file != new_file:
        # Intentamos borrar usando el storage backend (django-cloudinary-storage)
        # O si es una referencia directa, cloudinary.uploader.destroy
        try:
            # Opción 1: storage.delete() si el backend está bien configurado
            old_file.delete(save=False) 
        except Exception as e:
            print(f"Error al eliminar imagen antigua de Cloudinary: {e}")

@receiver(post_delete, sender=InventarioProducto)
def eliminar_imagen_al_borrar_producto(sender, instance, **kwargs):
    """
    Elimina la imagen de Cloudinary cuando se borra el registro permanentemente.
    Nota: Si usas soft-delete (is_active=False), esto no se ejecutará.
    """
    if instance.imagen:
        try:
            instance.imagen.delete(save=False)
        except Exception as e:
            print(f"Error al eliminar imagen tras borrar producto: {e}")
