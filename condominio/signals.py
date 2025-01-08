from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil
from django.contrib.auth.models import Group
from .models import PerfilUsuario

@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    instance.perfil.save()


# Función para asignar propietarios al grupo "Propietarios"
def asignar_grupo_propietario():
    grupo_propietarios, created = Group.objects.get_or_create(name="Propietarios")
    
    # Aquí se añaden todos los propietarios al grupo "Propietarios"
    propietarios = PerfilUsuario.objects.filter(tipo_usuario="propietario")
    for propietario in propietarios:
        propietario.user.groups.add(grupo_propietarios)

# Conectamos la señal post_save a la función
@receiver(post_save, sender=PerfilUsuario)
def asignar_grupo_a_propietario(sender, instance, created, **kwargs):
    # Solo asignamos al grupo cuando se crea un perfil de tipo "propietario"
    if created and instance.tipo_usuario == 'propietario':
        grupo_propietarios, created = Group.objects.get_or_create(name="Propietarios")
        instance.user.groups.add(grupo_propietarios)