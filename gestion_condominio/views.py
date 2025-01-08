from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def registro_residente(request):
    return render(request, 'Registro_residente.html')

def login_residente(request):
    return render(request, 'Login_residente.html')

def index(request):
    return render(request, 'base.html')

def recuperar_contraseña(request):
    return render(request, 'recuperar_contraseña.html')

def cambiar_contraseña(request):
    return render(request, 'cambiar_contraseña.html')