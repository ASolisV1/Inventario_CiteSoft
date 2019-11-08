from ..models import Miembros
from ..forms import SolicitarRegistroForm
from django.shortcuts import render, redirect
from django.contrib import messages
import re
from django.contrib.auth.models import Group, User
import random
# Formulario o vistas que redirigen a los templates disponible para un usuario que no ha iniciado sesión o que es externo al sistema

def login(request):
    return render(request, 'Registro/login.html')

def solicitar_cuenta_form(request):
    if request.method == 'POST':
        formSolicitud = SolicitarRegistroForm(request.POST);
        if (formSolicitud.is_valid()):
            data = formSolicitud.data
            if re.match("[\d]{8}", data['username']):
                if len(data['username']) == 8:
                    print(data['username'])
                    if (not User.objects.filter(email=data['email']).exists()):
                        userGuardado = formSolicitud.save()
                        userGuardado.is_active = bool(0)
                        userGuardado.save()
                        # Crear Miembro
                        miembroAGuardar = Miembros(user=userGuardado,
                                               nombre=data['first_name'].upper(),
                                               apellido=data['last_name'].upper(),
                                               dni=data['username'],
                                               telefono="",
                                               correo=data['email'], 
                                               aleatorio = ''.join(random.choice('0123456789ABCDEF') for i in range(20)))
                        miembroAGuardar.save()
                        grupo = Group.objects.get(name='miembro_grupo')
                        grupo.user_set.add(userGuardado)
                        messages.info(request, 'Solicitud enviada. Enviaremos una respuesta a su correo en breve.')
                        return redirect('/inventario/')
                    else:
                        messages.error(request, 'Su Correo electrónico ya se encuentra registrado.')
                else:
                    messages.error(request, 'Su DNI es incorrecto.')
            else:
                messages.error(request, 'Su DNI es incorrecto.')            
        else:
            # Mostrar mensaje
            messages.error(request, 'Su DNI ya se encuentra registrado.')            
    else:
        formSolicitud = SolicitarRegistroForm()

    return render(request, 'Registro/solicitar.html', {'formSolicitud': formSolicitud })

def inicio_funcion(request):
    if pertenece_miembro_grupo(request.user):
        return redirect('/inventario/inicio/')
    else:
        return redirect('/inventario/inicioadmin/')


def pertenece_miembro_grupo(user):
    return user.groups.filter(name='miembro_grupo').exists()
