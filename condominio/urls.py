from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views
from condominio import views
app_name= "condominio"


urlpatterns = [
     path('', views.index, name='index'),
    path('login_residente', views.login_residente, name='login_residente'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registro_residente', views.registro_residente, name='registro_residente'),
    path('cambiar_contraseña/<str:uidb64>/<str:token>/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('recuperar_contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),
    path('historial_pago/', views.historial_pago, name='historial_pago'),
    path('realizar_pago/', views.realizar_pago, name='realizar_pago'),
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('salida/', views.salida, name= 'salida'),
    path('enviar-notificaciones/', views.enviar_notificaciones, name='enviar_notificaciones'),
      ]
