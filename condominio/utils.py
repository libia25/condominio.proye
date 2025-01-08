from .models import HistorialCambio

def registrar_cambio(modelo, objeto_id, usuario, descripcion_cambio):
    HistorialCambio.objects.create(
        modelo=modelo,
        objeto_id=objeto_id,
        usuario=usuario,
        cambio=descripcion_cambio
    )