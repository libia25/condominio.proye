"""gestion_condominio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from condominio.views import custom_404

# Configura el manejador de error 404
# handler404 = 'condominio.views.custom_404'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),  
    path('condominio/', include('condominio.urls'))
]

# Esta línea es suficiente para servir archivos estáticos en DEBUG=True
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
