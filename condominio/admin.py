from django.contrib import admin
from .models import Departamento, Residente, MovimientoDePago, Pago, Factura, Servicio, Mantenimiento, Edificio, Notificacion, HistorialCambio
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.utils.dateparse import parse_date

# Define una clase de AdminSite personalizada
class MyAdminSite(admin.AdminSite):
    site_header = 'Administración del Condominio'
    site_title = 'Condominio'
    
    def get_model_perms(self, request, model):
        """Control de permisos para mostrar ciertos modelos."""
        return super().get_model_perms(request, model)

admin_site = MyAdminSite()
admin.site = admin_site

# Registrar los modelos
admin.site.register(MovimientoDePago)
admin.site.register(Servicio)
admin.site.register(Edificio)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'piso', 'nombre')  # Asegúrate de que los campos se muestran en el admin

admin.site.register(Departamento, DepartamentoAdmin)
# Registro del modelo Residente en el admin
@admin.register(Residente)
class ResidenteAdmin(admin.ModelAdmin):
    list_display = ('user', 'documento_identidad', 'nacionalidad', 'telefono', 'departamento')
admin.site.register(Residente, ResidenteAdmin)

# Personalizando la visualización de los Pagos
class PagoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_monto', 'get_fecha_emision', 'get_fecha_vencimiento', 'estado', 'get_metodo_pago')

    def get_monto(self, obj):
        return obj.monto
    get_monto.short_description = 'Monto'

    def get_metodo_pago(self, obj):
        return obj.metodo_pago
    get_metodo_pago.short_description = 'Método de Pago'

    def get_fecha_emision(self, obj):
        if obj.fecha_emision:
            return obj.fecha_emision.strftime('%d-%m-%Y')  # Asegúrate de que la fecha esté en el formato correcto
        return 'No disponible'
    get_fecha_emision.short_description = 'Fecha de Emisión'

    def get_fecha_vencimiento(self, obj):
        if obj.fecha_vencimiento:
            return obj.fecha_vencimiento.strftime('%d-%m-%Y')  # Asegúrate de que la fecha esté en el formato correcto
        return 'No disponible'
    get_fecha_vencimiento.short_description = 'Fecha de Vencimiento'

admin.site.register(Pago, PagoAdmin)

class FacturaAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'monto_total', 'descripcion', 'fecha', 'estado_pago')

    def estado_pago(self, obj):
        return obj.estado_pago  # Muestra el estado calculado de la factura
    estado_pago.short_description = 'Estado de Pago'

admin.site.register(Factura, FacturaAdmin)

# Personalizando la visualización de los Mantenimientos
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'descripcion', 'get_departamento', 'estado')

    def get_departamento(self, obj):
        # Asumiendo que 'residente' tiene un campo 'departamento'
        return obj.residente.departamento.nombre if obj.residente.departamento else 'Sin departamento'
    get_departamento.short_description = 'Departamento'

admin.site.register(Mantenimiento, MantenimientoAdmin)
# Personalizando la visualización de las Notificaciones
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'mensaje', 'leido', 'fecha_creacion')
    search_fields = ('mensaje', 'usuario__username')
    list_filter = ('leido',)

admin.site.register(Notificacion, NotificacionAdmin)

# Personalizando la visualización del Historial de Cambios
class HistorialCambioAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'objeto_id', 'usuario', 'cambio', 'fecha_cambio')
    search_fields = ('modelo', 'cambio', 'usuario__username')

admin.site.register(HistorialCambio, HistorialCambioAdmin)

