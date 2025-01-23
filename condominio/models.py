from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models import Sum



class Departamento(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)  # Número del departamento
    piso = models.IntegerField()  # Piso al que pertenece
    nombre = models.CharField(max_length=100, blank=True)  # Opcional, para un nombre adicional

    def __str__(self):
        return f"Departamento {self.numero} - Piso {self.piso}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Residente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="residente")
    departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)
    documento_identidad = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=2, choices=[('V', 'Venezolano'), ('E', 'Extranjero')])
    telefono = models.CharField(max_length=20)
    

    def __str__(self):
        return self.user.username  # Nombre de usuario del residente




class Servicio(models.Model):
    descripcion = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)  # Permite activar/desactivar servicios
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion



class Mantenimiento(models.Model):
    residente = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateField()
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE) 
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(
        max_length=50,
        choices=[('Pendiente', 'Pendiente'), ('Aprobado', 'Aprobado'), ('Rechazado', 'Rechazado')],
        default='Pendiente'
    )

    def __str__(self):
        return f"Mantenimiento - {self.descripcion[:20]} ({self.estado})"



class Pago(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pagos")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    servicios = models.ManyToManyField(Servicio)
    mantenimientos = models.ManyToManyField(Mantenimiento)
    metodo_pago = models.CharField(max_length=50)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(
        max_length=50,
        choices=[('Pendiente', 'Pendiente'), ('Pagado', 'Pagado')],
        default='Pendiente'
    )
    fecha_emision = models.DateField(auto_now_add=True)
    saldo_pendienteP = models.FloatField(default=0)

    def __str__(self):
        return f"Pago {self.id} - {self.estado}"


class Factura(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Asegúrate de tener este campo
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('Pagado', 'Pagado')])
    fecha = models.DateField()
    pago = models.ForeignKey(Pago, null=True, blank=True, on_delete=models.SET_NULL)  # Relación con Pago
    saldo_pendienteF = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda primero el objeto para que tenga un ID

        # Calcular el total pagado de los pagos relacionados
        pagos_realizados = Pago.objects.filter(factura=self).aggregate(total_pagado=Sum('monto_pagado'))['total_pagado'] or Decimal('0.00')
        
        # Calcular el saldo pendiente restando el monto pagado del monto total
        self.saldo_pendienteF = self.monto_total - (self.monto_pagado + pagos_realizados)
        super().save(update_fields=['saldo_pendienteF'])  # Solo actualiza el saldo pendienteF

    def __str__(self):
        return f"Factura {self.id} - {self.descripcion}"
    



class Solicitud(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="solicitudes")
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.titulo
    
# Modelo MovimientoDePago
class MovimientoDePago(models.Model):
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=50)  # Ejemplo: 'Ingreso', 'Egreso'
    descripcion = models.TextField(blank=True, null=True)


# Modelo Edificio
class Edificio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='edificios')

# Modelo Notificacion
class Notificacion(models.Model):
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    destinatarios = models.ManyToManyField(User, related_name='notificaciones_recibidas')
    leida = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

# Modelo HistorialCambio
class HistorialCambio(models.Model):
    modelo = models.CharField(max_length=100)  # Nombre del modelo afectado
    objeto_id = models.PositiveIntegerField()  # ID del objeto afectado
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cambio = models.TextField()  # Descripción del cambio
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cambio en {self.modelo} (ID: {self.objeto_id}) por {self.usuario.username} en {self.fecha_cambio}"



