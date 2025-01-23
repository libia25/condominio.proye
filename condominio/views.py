import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.db import models 
from .forms import NotificacionResidenteForm
from .models import Residente
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum, F
from datetime import timedelta
from .models import Departamento, Pago, Factura, Servicio, Mantenimiento, Edificio, Residente,Notificacion,MovimientoDePago,Residente, Solicitud
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from decimal import Decimal
from django.utils import timezone
from .forms import SolicitudForm
from django.contrib.auth.decorators import user_passes_test




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registro_residente(request):
    departamentos = Departamento.objects.all()  # Obtener todos los departamentos

    if request.method == 'POST':
        # Recibir los datos del formulario
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        username = request.POST.get('username', '')
        documento_identidad = request.POST.get('documento_identidad', '')
        nacionalidad = request.POST.get('nacionalidad', '')
        telefono = request.POST.get('telefono', '')
        departamento_id = request.POST.get('departamento', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        email = request.POST.get('email', '')  # Obtener el correo electrónico del formulario

        try:
            # Validación de la contraseña
            if password != password_confirm:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('condominio:index')  # Redirigir al index

            # Verificar que todos los campos estén completos
            if not nombre or not apellido or not username or not documento_identidad or not telefono or not departamento_id or not password or not email:
                messages.error(request, 'Todos los campos son obligatorios.')
                return redirect('condominio:index')  # Redirigir al index

            # Verificar si el nombre de usuario ya existe
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya existe.')
                return redirect('condominio:index')  # Redirigir al index

            # Verificar si el documento de identidad ya existe
            if Residente.objects.filter(documento_identidad=documento_identidad).exists():
                messages.error(request, 'La cédula ya está registrada.')
                return redirect('condominio:index')  # Redirigir al index

            # Crear el usuario de Django, incluyendo el correo electrónico
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=nombre,
                last_name=apellido,
                email=email  # Asignar el correo electrónico al campo 'email' del usuario
            )

            # Crear el residente y asociarlo al departamento
            departamento = Departamento.objects.get(id=departamento_id)
            residente = Residente(
                user=user,
                documento_identidad=documento_identidad,
                nacionalidad=nacionalidad,
                telefono=telefono,
                departamento=departamento
            )
            residente.save()

            # Si todo es exitoso, redirigir al login
            messages.success(request, 'Residente registrado exitosamente.')
            return redirect('condominio:login_residente')

        except Exception as e:
            # Si ocurre un error inesperado, redirigir al index
            messages.error(request, f'Error inesperado: {str(e)}')
            return redirect('condominio:index')  # Redirigir al index

    # Renderizar la página con los departamentos y encabezados de no-caché
    response = render(request, 'registro_residente.html', {'departamentos': departamentos})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response



def recuperar_contraseña(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Buscar el usuario por su email
            user = User.objects.get(email=email)
            
            # Generar token de recuperación de contraseña
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))  # Codificar el ID del usuario
            
            # Crear URL de recuperación
            reset_url = request.build_absolute_uri(
                reverse('condominio:cambiar_contraseña', kwargs={'uidb64': uid, 'token': token})
            )
            
            # Enviar el correo electrónico con el enlace de recuperación
            subject = 'Recuperación de contraseña'
            message = f'Para restablecer tu contraseña, haz clic en el siguiente enlace:\n\n{reset_url}'
            send_mail(subject, message, 'ricarberri@gmail.com', [email])  # Usar el correo configurado en settings.py
            
            # Mensaje de éxito
            messages.success(request, 'Las instrucciones para recuperar tu contraseña han sido enviadas a tu correo.')
            return redirect('condominio:login_residente')  # Redirigir a la página de login
            
        except User.DoesNotExist:
            messages.error(request, 'No se ha encontrado una cuenta asociada a este correo electrónico.')

    return render(request, 'Recuperar_contraseña.html')


def cambiar_contraseña(request, uidb64, token):
    try:
        # Decodificar uid para obtener el usuario
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                # Validar si la contraseña ya está en uso
                if user.check_password(new_password):
                    form.add_error('new_password1', 'La nueva contraseña no puede ser igual a la actual.')
                else:
                    form.save()
                    messages.success(request, "Tu contraseña ha sido cambiada con éxito.")
                    return redirect('index')
            # Formulario inválido, re-renderizar la página
            return render(request, 'cambiar_contraseña.html', {'form': form, 'uidb64': uidb64, 'token': token})
        else:
            form = SetPasswordForm(user)
            return render(request, 'cambiar_contraseña.html', {'form': form, 'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, "El enlace de recuperación de contraseña es inválido o ha expirado.")
        return redirect('condominio:recuperar_contraseña')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_residente(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Intentar autenticar al usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Si el usuario existe y las credenciales son correctas
            login(request, user)
            return redirect('condominio:dashboard')  # Redirigir al dashboard
        else:
            # Si las credenciales son incorrectas, mostrar un mensaje de error
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
            return redirect('condominio:login_residente')  # Redirigir al login nuevamente
    
    return render(request, 'login_residente.html')

@login_required
def realizar_pago(request):
    # Obtener el residente y el departamento del usuario actual
    residente = Residente.objects.get(user=request.user)
    departamento = residente.departamento
    
    # Obtener servicios y mantenimientos pendientes
    servicios = Servicio.objects.filter(departamento=departamento, activo=True)
    mantenimientos = Mantenimiento.objects.filter(departamento=departamento, estado='Pendiente')
    
    # Obtener facturas y pagos previos
    facturas = Factura.objects.filter(departamento=departamento, estado='Pendiente')
    total_pagado = Pago.objects.filter(departamento=departamento).aggregate(total=Sum('monto_pagado'))['total'] or Decimal('0.00')
    saldo_pendienteF = facturas.aggregate(saldo=Sum('saldo_pendienteF'))['saldo'] or Decimal('0.00')

    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        monto_pagado = Decimal(request.POST.get('monto_pagado', '0.00'))
        servicios_seleccionados = request.POST.getlist('servicios')
        mantenimientos_seleccionados = request.POST.getlist('mantenimientos')

        # Obtener o crear una factura pendiente
        factura = facturas.first()
        if not factura:
            # Validar selección solo si no hay factura pendiente
            if not servicios_seleccionados and not mantenimientos_seleccionados:
                messages.error(request, "Debe seleccionar al menos un servicio o mantenimiento.")
                return redirect('condominio:realizar_pago')

            # Calcular total seleccionado
            servicios_qs = Servicio.objects.filter(id__in=servicios_seleccionados)
            mantenimientos_qs = Mantenimiento.objects.filter(id__in=mantenimientos_seleccionados)
            total_servicios = servicios_qs.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
            total_mantenimientos = mantenimientos_qs.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
            total_seleccionado = total_servicios + total_mantenimientos

            # Crear una nueva factura
            factura = Factura.objects.create(
                departamento=departamento,
                monto_total=total_seleccionado,
                saldo_pendienteF=total_seleccionado,
                estado='Pendiente',
                descripcion='Factura generada automáticamente',
                fecha=timezone.now(),
                usuario=request.user
            )
        else:
            # Si ya existe una factura, no es necesario seleccionar servicios/mantenimientos
            total_seleccionado = factura.saldo_pendienteF

        # Validar el monto del pago
        if monto_pagado > total_seleccionado:
            messages.error(request, "El monto pagado no puede superar el saldo pendiente.")
            return redirect('condominio:realizar_pago')

        # Actualizar factura según el monto pagado
        if monto_pagado >= factura.saldo_pendienteF:
            factura.monto_pagado += monto_pagado
            factura.saldo_pendienteF = Decimal('0.00')
            factura.estado = 'Pagado'
        else:
            factura.monto_pagado += monto_pagado
            factura.saldo_pendienteF -= monto_pagado

        factura.save()

        # Crear registro del pago
        pago = Pago.objects.create(
            usuario=request.user,
            departamento=departamento,
            monto=total_seleccionado,
            metodo_pago=metodo_pago,
            monto_pagado=monto_pagado,
            saldo_pendienteP=factura.saldo_pendienteF,
            estado=factura.estado
        )

        # Asociar servicios y mantenimientos al pago si se seleccionaron
        if not facturas.exists():
            servicios_qs = Servicio.objects.filter(id__in=servicios_seleccionados)
            mantenimientos_qs = Mantenimiento.objects.filter(id__in=mantenimientos_seleccionados)
            pago.servicios.set(servicios_qs)
            pago.mantenimientos.set(mantenimientos_qs)

            # Marcar mantenimientos como pagados
            mantenimientos_qs.update(estado='Pagado')

        # Mensaje de éxito
        if factura.estado == 'Pagado':
            messages.success(request, "Pago realizado exitosamente.")
        else:
            messages.success(request, f"Pago parcial realizado. Saldo pendiente: ${factura.saldo_pendienteF:.2f}")

        return redirect('condominio:dashboard')

    return render(request, 'realizar_pago.html', {
        'servicios': servicios,
        'mantenimientos': mantenimientos,
        'departamento': departamento,
        'total_pagado': total_pagado,
        'saldo_pendienteF': saldo_pendienteF,  # Aquí se pasa el saldo pendiente de factura
    })

@login_required
def dashboard(request):
    try:
        # Obtener el Residente correspondiente al usuario actual
        residente = Residente.objects.get(user=request.user)
        departamento = residente.departamento
    except Residente.DoesNotExist:
        return redirect('condominio:sin_residencia')
    except Departamento.DoesNotExist:
        return redirect('condominio:sin_departamento')

    servicios = Servicio.objects.all()
    mantenimientos = Mantenimiento.objects.all()
    
    # Ajustar el total pendiente para reflejar el saldo pendiente
    total_pendiente = Factura.objects.filter(departamento=departamento, estado='Pendiente').aggregate(total=Sum('saldo_pendienteF'))['total'] or Decimal('0.00')

    # Calcular el total pagado de las facturas
    total_pagado = Pago.objects.filter(departamento=departamento).aggregate(total=Sum('monto_pagado'))['total'] or Decimal('0.00')

    # Sumar montos de servicios pendientes
    servicios_pendientes = Servicio.objects.filter(departamento=departamento, activo=True)
    total_servicios_pendientes = servicios_pendientes.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')

    # Sumar montos de mantenimientos pendientes
    mantenimientos_pendientes = Mantenimiento.objects.filter(departamento=departamento, estado='Pendiente')
    total_mantenimientos_pendientes = mantenimientos_pendientes.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
   
    # Obtener las últimas facturas
    ultimas_facturas = Factura.objects.filter(departamento=departamento).order_by('-fecha')[:5]

    # Obtener los últimos pagos
    ultimos_pagos = Pago.objects.filter(departamento=departamento).order_by('-fecha_emision')[:5]

    # Pasar todo al contexto
    context = {
        'servicios': servicios,
        'mantenimientos': mantenimientos,
        'total_pendiente': total_pendiente,
        'total_pagado': total_pagado,
        'total_servicios_pendientes': total_servicios_pendientes,
        'total_mantenimientos_pendientes': total_mantenimientos_pendientes,
        'ultimas_facturas': ultimas_facturas,
        'ultimos_pagos': ultimos_pagos,
    }

    return render(request, 'dashboard.html', context)


def es_administrador(user):
    return user.is_staff or user.is_superuser

@user_passes_test(es_administrador)
def enviar_notificaciones(request):
    residentes = Residente.objects.all()
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        mensaje = request.POST.get('mensaje')
        destinatarios = request.POST.getlist('destinatarios')
        
        if not titulo or not mensaje or not destinatarios:
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'condominio/enviar_notificaciones.html', {'residentes': residentes})
        
        try:
            notificacion = Notificacion.objects.create(
                titulo=titulo,
                mensaje=mensaje
            )
            # Agregar los destinatarios seleccionados
            usuarios_destinatarios = User.objects.filter(id__in=destinatarios)
            notificacion.destinatarios.set(usuarios_destinatarios)
            
            messages.success(request, 'Notificación enviada exitosamente')
            return redirect('condominio:dashboard')
        except Exception as e:
            messages.error(request, f'Error al enviar la notificación: {str(e)}')
    
    return render(request, 'condominio/enviar_notificaciones.html', {'residentes': residentes})

def index(request):
    return render(
        request,
        'index.html',    
    )
    

@login_required
def historial_pago(request):
    pagos = Pago.objects.filter(usuario=request.user)
    return render(request, 'historial_pago.html', {'pagos': pagos})
    
def salida(request):
    # Limpia la sesión
    request.session.flush()
    # Redirige al login
    return render(request, 'salida.html')

# def custom_404(request, exception, template_name='404.html'):
#     return render(request, template_name)

def solicitudes(request):
    mensaje = ""  # Inicializamos la variable mensaje

    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user  # Asociamos la solicitud al usuario
            solicitud.save()  # Guardamos la solicitud en la base de datos
            
            mensaje = "¡Tu solicitud ha sido enviada correctamente!"  # Mensaje de éxito
            return redirect('condominio:dashboard')  # Redirigir al dashboard
    else:
        form = SolicitudForm()

    return render(request, 'solicitudes.html', {'form': form, 'mensaje': mensaje})

