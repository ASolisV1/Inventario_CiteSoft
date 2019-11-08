from django.views.generic import DetailView, ListView, UpdateView, CreateView, View 
from ..models import recursos, Miembros, Historial_Recursos, EstadoRecurso, Entidad, Documento, Cargos, Proyectos, Historial_Proyecto, EstadoProyecto, ResultadoProyecto, Recurso_Documento, Miembro_Proyecto, Recurso_Proyecto, MiembroProyecto_RecursoProyecto
from ..forms import recursosForm, MiembrosForm, Historial_RecursosForm, EstadoRecursoForm, EntidadForm, DocumentoForm, CargosForm, ProyectosForm, Historial_ProyectoForm, EstadoProyectoForm, ResultadoProyectoForm, Recurso_DocumentoForm, Miembro_ProyectoForm, Recurso_ProyectoForm, MiembroProyecto_RecursoProyectoForm
from django.shortcuts import render
from django.contrib import messages
from Inventario.forms import RegistrarProyectoForm, CoordinadorProyectoForm, \
    MiembroProyectoForm, buscarRecursosForm, UserForm, recursoEditForm,\
    MiembrosRegistro, buscarMiembrosForm, ProyectosEditForm, buscarProyectosForm,\
    MiembrosEditForm
import re
from django.contrib.auth.models import Group, User
from django.core.mail.message import EmailMultiAlternatives
from django.http.response import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.sites.requests import RequestSite
import random
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import redirect
from datetime import datetime, date
from django.db.utils import IntegrityError
import logging
import reportlab
from reportlab.pdfgen import canvas
from django.conf import settings
from io import BytesIO

##TESTEAR 
## De debe hacer pruebas segun cada comentario en las funciones

def inicio(request):
    return render(request, 'index.html')

def get_user_profile(request, username):
    admin = User.objects.get(username=username)
    return render(request, 'Usuario/profile.html', {"admin":admin})


def listar_solicitudes(request):
    solicitudes = Miembros.objects.filter(estado_miembro='PENDIENTE')
    contexto = {'solicitudes' : solicitudes }
    return render(request, 'Registro/solicitud.html', contexto)

def aprobar_solicitud(request, idUser):
    user = User.objects.get(id=idUser)
    miembro = Miembros.objects.get(user_id=idUser)
    subject, from_email, to = 'Solicitud CiTeSoft', 'CiTeSoft', user.email
    text_content = 'MENSAJE IMPORTANTE'
    site_name = RequestSite(request).domain
    print(site_name)
    html_content = '<h2>Su solicitud ha sido aprobada.</h2> <p>Por favor complete el siguiente formulario para culminar su registro:</p> <a href="http://' + site_name + '/inventario/Inventario/miembros/registrar/' + str(miembro.id) + '/'+ miembro.aleatorio +'/">PRESIONE AQUÍ</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # # Cambiando el estado del usuario
    # # de PENDIENTE a APROBADO
    miembro.estado_miembro = 'APROBADO'
    miembro.save()
    
    return redirect('/inventario/solicitudes')

def rechazar_solicitud(request, idUser):
    user = User.objects.get(id=idUser)
    subject, from_email, to = 'Solicitud CiTeSoft', 'CiTeSoft', user.email
    text_content = 'MENSAJE IMPORTANTE'
    html_content = '<h2>Su solicitud ha sido rechazada. Para más información enviar un correo electrónico a citesoft@unsa.edu.pe.</h2>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    # Eliminar miembro
    user.delete()
    return redirect('/inventario/solicitudes')


def registrarMiembro(request, idUser, aleatorio):
    try:
        miembro = Miembros.objects.get(id=idUser, aleatorio=aleatorio, estado_miembro='APROBADO')
        user = User.objects.get(id=miembro.user_id)
        if request.method == 'GET':
            formMiembro = MiembrosForm(instance=miembro)
            formUser = UserForm(instance=user)
        else:
            formMiembro = MiembrosForm(request.POST, request.FILES, instance=miembro)
            formUser = UserForm(request.POST, instance=user)
            if formMiembro.is_valid():
                ## actualizando datos de la tabla MIEMBROS
                miem = formMiembro.save()
                miem.foto = request.FILES.get('fotoMiembro', 'images/miembros/None/no-img.jpg')
                miem.estado_miembro = 'ACTIVO'
                miem.save()
                
                ## Actualizando datos de la tabla USER
                user.password = make_password(formUser.data['password'])
                user.is_active = bool(1)
                user.save()
                messages.info(request, 'Registro completo. Use su DNI como usuario para iniciar sesión.')
                
                ## Registrando miembro a proyecto citesoft
                proyectoCitesoft = Proyectos.objects.get(nombre = 'CITESOFT')
                cargo = Cargos.objects.get(descripcion='PERSONAL DE APOYO')
                
                registrarMiembroCitesoft = Miembro_Proyecto(descripcion = 'Inició en el proyecto',
                                                            fecha_miembro_proyecto = formMiembro.data['fecha_ingreso'],
                                                            estado_miembro_proyecto = 'ACTIVO',
                                                            idCargo = cargo,
                                                            idMiembro = miem,
                                                            idProyecto = proyectoCitesoft
                                                            )
                registrarMiembroCitesoft.save()
                
                return redirect('/inventario/')
        return render(request, 'Inventario/miembros_form.html', {'formMiembro':formMiembro, 'formUser':formUser, 'miembro': miembro})
    except Miembros.DoesNotExist:
        messages.info(request, 'Ud. no tiene permisos para visualizar estos datos.')
        return redirect('/inventario/')

def registrarRecursos(request):
    if request.method == 'POST':
        form = recursosForm(request.POST, request.FILES)        
        data = form.data
        print(data)
        
        ## Verificamos si estamos recibiendo información del primer formulario
        
        if (data['form'] == '1'): ##Estamos en el primer formulario (Documentos)
            ## Guardamos los 5 documentos Factura/Boleta
            ## Guía de Remisión, Orden de Compra, Acta de Conformidad, Comprobante de Salida
            documentos = []
            ## FACTURA/BOLETA
            ## Sólo si se agregó una fatura, se guardará
            ## print(request.FILES.get('factura', False))
            if request.FILES.get('factura', False):
                name = str(request.FILES.get('factura'))
                Factura = Documento(codigo_documento = 'factura_' + name,
                                fecha_emision = data['fecha_ingreso'],
                                ruta_pdf = request.FILES.get('factura'),
                                estado = 'ACTIVO',
                                tipo = 'FACTURA_BOLETA',
                                entidad = Entidad.objects.get(razon_social='UNSA')
                                )
                ## print(Factura)
                Factura.save()
                documentos.append(Factura)
            
            if request.FILES.get('guia', False):
                name = str(request.FILES.get('guia'))
                Guia = Documento(codigo_documento = 'guia_' + name,
                                fecha_emision = data['fecha_ingreso'],
                                ruta_pdf = request.FILES.get('guia'),
                                estado = 'ACTIVO',
                                tipo = 'GUIA DE REMISION',
                                entidad = Entidad.objects.get(razon_social='UNSA')
                                )
                ## print(Guia)
                Guia.save()
                documentos.append(Guia)
            
            if request.FILES.get('orden', False):
                name = str(request.FILES.get('orden'))
                Orden = Documento(codigo_documento = 'orden_' + name,
                                fecha_emision = data['fecha_ingreso'],
                                ruta_pdf = request.FILES.get('orden'),
                                estado = 'ACTIVO',
                                tipo = 'ORDEN DE COMPRA',
                                entidad = Entidad.objects.get(razon_social='UNSA')
                                )
                ## print(Orden)
                Orden.save()
                documentos.append(Orden)    
                
            if request.FILES.get('conformidad', False):
                name = str(request.FILES.get('conformidad'))
                Conformidad = Documento(codigo_documento = 'conformidad_' + name,
                                fecha_emision = data['fecha_ingreso'],
                                ruta_pdf = request.FILES.get('conformidad'),
                                estado = 'ACTIVO',
                                tipo = 'ACTA DE CONFORMIDAD',
                                entidad = Entidad.objects.get(razon_social='UNSA')
                                )
                ## print(Conformidad)
                Conformidad.save()
                documentos.append(Conformidad)
             
            if request.FILES.get('comprobante', False):
                name = str(request.FILES.get('comprobante'))
                Comprobante = Documento(codigo_documento = 'comprobante_' + name,
                                fecha_emision = data['fecha_ingreso'],
                                ruta_pdf = request.FILES.get('comprobante'),
                                estado = 'ACTIVO',
                                tipo = 'COMPROBANTE DE SALIDA',
                                entidad = Entidad.objects.get(razon_social='UNSA')
                                )
                ## print(Comprobante)
                Comprobante.save()
                documentos.append(Comprobante)
                
            print('registrados')
            contexto = {'documentos' : documentos, 'form':form, 'fecha_ingreso' : data['fecha_ingreso']}
            
            return render(request, 'Recurso/registro_recurso2.html', contexto)
        
        else:
            ## Formulario 2
            print('Formulario 2')
            
            
            ## Guardamos el recurso recibido
            
            codsPatrimonio = data.getlist('cod_1_1')
            numsProducto = data.getlist('cod_1_2')
            numsSerie = data.getlist('cod_1_3')
            docs = data.getlist('documentos')
            print(docs)
            documentos = []
            i = 0
            for cod in codsPatrimonio:
                print(cod+' '+numsProducto[i]+' '+numsSerie[i])
                recursoNuevo = recursos(cod_patrimonio = cod,
                                        nro_producto = numsProducto[i],
                                        nro_serie = numsSerie[i],
                                        nombre = data['nombre'].upper(),
                                        foto = request.FILES.get('foto', False),
                                        fecha_ingreso = data['fecha_ingreso'],
                                        caracteristicas = data['caracteristicas'].upper())
                recursoNuevo.save()
                
                ## registrar al proyecto Citesoft
                proyecto = Proyectos.objects.get(nombre = 'CITESOFT')
                
                recursoProyecto = Recurso_Proyecto(descripcion = 'Se añadió al proyecto CITESOFT',
                                                   estado = 'ACTIVO',
                                                   fecha_recurso_proyecto = data['fecha_ingreso'],
                                                   idProyecto = proyecto,
                                                   idRecurso = recursoNuevo
                                                   )
                recursoProyecto.save()
                
                for doc in docs:
                    print(doc)
                    documento = Documento.objects.get(id=doc)
                    documentos.append(documento)
                    RecursoDocumento = Recurso_Documento(idDocumento = documento,
                                                         idRecurso = recursoNuevo
                                                         )
                    RecursoDocumento.save()
                              
                i = i + 1
                
            
            if (data['form'] == '2'): ## Finalizar
                return redirect('Inventario_recursos_listar')
            print(documentos)
            contexto = {'documentos' : documentos, 'form':form, 'fecha_ingreso' : data['fecha_ingreso']}
            return render(request, 'Recurso/registro_recurso2.html', contexto) ## form = 3   
        #messages.info(request, 'Registro del recurso completo.')     
        # 
    else:
        form = recursosForm()
    
    return render(request, 'Recurso/registro_recurso1.html', {'form': form })

def registrarProyecto(request):
    if request.method == 'POST':
        formProyecto = RegistrarProyectoForm(request.POST, request.FILES)
        formCoordinador = CoordinadorProyectoForm(request.POST)
        if (formProyecto.is_valid()):
            proyecto = Proyectos(codigo = formProyecto.data['codigo'],
                                 nombre = formProyecto.data['nombre'].upper(),
                                 descripcion = formProyecto.data['descripcion'].upper(),
                                 fecha_inicio = formProyecto.data['fecha_inicio'],
                                 foto = request.FILES.get('foto', 'images/proyectos/None/no-img.jpg')) ##formProyecto.save()
            proyecto.save()
            cargo = Cargos.objects.get(descripcion='COORDINADOR')
            coordinador = Miembros.objects.get(id=formCoordinador.data['idMiembro'])
            coordinadorProyecto = Miembro_Proyecto(descripcion='Inició en el proyecto',
                                                   fecha_miembro_proyecto=formProyecto.data['fecha_inicio'],
                                                   estado_miembro_proyecto='ACTIVO',
                                                   idCargo=cargo,
                                                   idMiembro=coordinador,
                                                   idProyecto=proyecto)
            coordinadorProyecto.save()
            cadena = '/inventario/Inventario/proyectos/detalle/' + str(proyecto.id) + '/'
            return redirect(cadena)
        else:
            print('Datos inválidos')
    else:
        formProyecto = RegistrarProyectoForm()
        formCoordinador = CoordinadorProyectoForm()
    return render(request, 'Proyecto/proyectos_form.html', {'formProyecto': formProyecto, 'formCoordinador': formCoordinador})

def detalleProyecto(request, idProyecto):
    try:
        proyecto = Proyectos.objects.get(id=idProyecto)
        miembros = Miembro_Proyecto.objects.filter(idProyecto=proyecto, estado_miembro_proyecto='ACTIVO').order_by('created')
        recursos = Recurso_Proyecto.objects.filter(idProyecto=proyecto, estado='ACTIVO').order_by('created')

        contexto = {'proyecto' : proyecto, 'miembros' : miembros, 'recursos': recursos}
        return render(request, 'Proyecto/proyecto_detalle.html', contexto)
    except Proyectos.DoesNotExist:
        proyecto = None
        contexto = {'proyecto' : proyecto }
        return render(request, 'Proyecto/proyecto_detalle.html', contexto)

def asignarMiembroProyecto(request, idProyecto):
    try:
        proyecto = Proyectos.objects.get(id=idProyecto)
        ## Buscamos a los miembros activos
        miembrosActivos = Miembros.objects.filter(estado_miembro='ACTIVO')
        
        # Filtramos los que ya estén en el proyecto
        miembros = []
        for m in miembrosActivos:
            if Miembro_Proyecto.objects.filter(idMiembro=m, idProyecto=proyecto).exists():
                continue
            else:
                miembros.append(m)

        if request.method == 'POST':
            form = MiembroProyectoForm(request.POST)
            if (form.is_valid()):
                
                ## Lo eliminaremos del proyecto citesoft (Cambiaremos estado a INACTIVO)
                proyectoCitesoft = Proyectos.objects.get(nombre='CITESOFT')
                miembro = Miembros.objects.get(id=form.data['idMiembro'])

                editarEstadoMiembroProyecto = Miembro_Proyecto.objects.get(idProyecto = proyectoCitesoft, idMiembro = miembro)
                editarEstadoMiembroProyecto.estado_miembro_proyecto = 'INACTIVO'
                editarEstadoMiembroProyecto.descripcion = form.data['descripcion'] + ' '+proyecto.nombre
                editarEstadoMiembroProyecto.save()
                
                print('Eliminado del proyecto Citesoft')
                
                ## print(request.POST.get('fecha_miembro_proyecto'))
                
                
                date = datetime.strptime(request.POST.get('fecha_miembro_proyecto'), "%d/%m/%Y").date()
                print(date)
                MiembroProyecto = Miembro_Proyecto(descripcion=form.data['descripcion'],
                                                   idProyecto=proyecto,
                                                   idCargo=Cargos.objects.get(id=form.data['idCargo']),
                                                   fecha_miembro_proyecto= date,
                                                   idMiembro=Miembros.objects.get(id=form.data['idMiembro']),
                                                   estado_miembro_proyecto='ACTIVO'
                                                   )
                MiembroProyecto.save()
                print(MiembroProyecto)
                
                cadena = '/inventario/Inventario/proyectos/detalle/' + str(proyecto.id) + '/'
                return redirect(cadena)
            else:
                print('error')
        else:
            form = MiembroProyectoForm()
        return render(request, 'Proyecto/asignar_miembro.html', {'form': form, 'proyecto':proyecto, 'miembros' : miembros })
    except Proyectos.DoesNotExist:
        return redirect('/inventario/')

def asignarRecursoProyecto(request, idProyecto):
    try:
        ## Proyecto al cual se va a asignar el recurso
        proyecto = Proyectos.objects.get(id=idProyecto)
        ## Todos los recursos que no pertenecen a algun proyecto 
        ## recursosSinAsignar = recursos.objects.filter(rn_recurso=None)
        ## Todos los recursos que pertenecen al proyecto CiTeSoft en estado ACTIVO
        #### Primero se obtiene el proyecto CiTeSoft, ignorando mayusculas y minusculas
        proyectoCiTeSoft = Proyectos.objects.filter(nombre__iexact='citesoft')[0].id
        #### Filtrar Recurso_Proyecto donde su proyecto sea CiTesoft 
        recursoProyectoDeCiTeSoftIDs = Recurso_Proyecto.objects.filter(idProyecto=proyectoCiTeSoft, estado='ACTIVO')
        ## .values_list('idRecurso', flat = True) ##t_Recurso_Proyecto.recursos.all() ##recursos.objects.filter(nombre__iregex=r'(citesoft|CiTeSoft|CITESOFT|Citesoft)')
        ## recursosDeCiTeSoft = recursos.objects.filter(pk__in=recursoProyectoDeCiTeSoftIDs)

        recursosDisponibles = recursoProyectoDeCiTeSoftIDs
        print(recursosDisponibles)

        if request.method == 'POST':
            # Formulario enviado
            form = Recurso_ProyectoForm(request.POST)

            # Fecha de asignación del proyecto
            print('hey')
            print(request.POST.get('fecha_recurso_proyecto'))
            print('heyyyyy')
            
            date = datetime.strptime(request.POST.get('fecha_recurso_proyecto'), "%Y-%m-%d").date()
            try:
                recursoExiste = recursos.objects.get(id=form.data['idRecurso'])
            except:
                print('No existe')
                return redirect('/inventario/')
            if not recursoExiste:
                print('id incorrecto')
                return redirect('/inventario/')

            # Registro de Recurso_Proyecto en el cual el recurso que se quiera asignar esta en un proyecto, en estado ACTIVO
            antiguoRecursoProyecto = Recurso_Proyecto.objects.filter(estado='ACTIVO',idRecurso=form.data['idRecurso'])

            # Si el recurso está asignado actualmente en el proyecto CiTeSoft
            # Cambiar el estado a INACTIVO
            if antiguoRecursoProyecto:
                inhabilitarRegistro = antiguoRecursoProyecto[0]
                inhabilitarRegistro.estado = 'INACTIVO'
                inhabilitarRegistro.save()
            
            ## Buscamos si el recurso seleccionado 
            recursoProyectoAnterior = Recurso_Proyecto.objects.filter(idRecurso = form.data['idRecurso'], idProyecto=idProyecto)
            
            if recursoProyectoAnterior:
                recursoProyectoAnterior[0].estado='ACTIVO'
                recursoProyectoAnterior[0].descripcion = 'Resignado a ' + str(proyecto.nombre)
                recursoProyectoAnterior[0].save()
                
            else:
                recursoAsignadoAProyecto = Recurso_Proyecto(descripcion = 'Asignado a ' + proyecto.nombre, 
                                                   estado = 'ACTIVO',
                                                   fecha_recurso_proyecto = date,
                                                   idProyecto = proyecto,
                                                   idRecurso = recursos.objects.get(id=form.data['idRecurso']))
                recursoAsignadoAProyecto.save()
                #print(recursoAsignadoAProyecto)
                
            
            cadena = '/inventario/Inventario/proyectos/detalle/' + str(proyecto.id) + '/'
            return redirect(cadena)
        else:
            form = Recurso_ProyectoForm()
        return render(request, 'Proyecto/asignar_recurso.html', {'form': form, 'proyecto':proyecto, 'recursos' : recursosDisponibles })
    except Proyectos.DoesNotExist as e:
        print(e)
        return redirect('/inventario/')

    
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Miembros.objects.filter(nombre=username).exists(),
        'objects' : serializers.serialize('json', Miembros.objects.filter(estado_miembro='PENDIENTE'), fields=['id', 'nombre'])
    }
    print(data)
    return JsonResponse(data)

def recursosListarView(request):
    if request.method == 'POST':
        form = buscarRecursosForm(request.POST)
        data = form.data
        nombre = data['nombre']
               
        recursoEsp = recursos.objects.filter(Q(nombre__contains=nombre.upper()) | Q(caracteristicas__contains=nombre.upper()), estado='ACTIVO')
        recurso = recursos.objects.filter(estado='ACTIVO')
        estadosRecurso = []
        for r in recurso:
            print(r.id)
            recursoProyecto = Recurso_Proyecto.objects.get(idRecurso=r, estado='ACTIVO')
            if MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto = recursoProyecto, estado='ACTIVO').exists():
                estadosRecurso.append('ASIGNADO')
            else:
                estadosRecurso.append('SIN ASIGNAR')
        
        print(estadosRecurso)
        juntos = zip(recurso, estadosRecurso)
                   
        contexto = {'recursoss':recurso,
                    'recursoEsp1':recursoEsp,
                    'juntos': juntos
                    }
        ## print(contexto)
        return render(request, 'Recurso/recursos.html', contexto)
    else:    
        recurso = recursos.objects.filter(estado='ACTIVO')
        listado = [True]
        estadosRecurso = []
        for r in recurso:
            recursoProyecto = Recurso_Proyecto.objects.get(idRecurso=r, estado='ACTIVO')
            # recursoProyecto = Recurso_Proyecto.objects.get(idRecurso=r)
            if MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto = recursoProyecto, estado='ACTIVO').exists():
                estadosRecurso.append('ASIGNADO')
            else:
                estadosRecurso.append('SIN ASIGNAR')
        
        juntos = zip(recurso, estadosRecurso)
        contexto = {'recursoss':recurso,
                    'juntos':juntos,
                    'listado':listado}
    return render(request, 'Recurso/recursos.html', contexto)

def recursosEditarView(request, idRecurso):
    try:
        recurso = recursos.objects.get(id=idRecurso)
        if request.method == 'GET':
            formRecurso = recursoEditForm(instance=recurso)
        else:
            formRecurso= recursoEditForm(request.POST, request.FILES, instance=recurso)
            recurso.cod_patrimonio = formRecurso.data['cod_patrimonio']
            recurso.nro_producto = formRecurso.data['nro_producto']
            recurso.nro_serie = formRecurso.data['nro_serie']
            recurso.nombre = formRecurso.data['nombre'].upper()
            
            if (request.FILES.get('foto', False)): ##  Si recibe una foto en el formulario la cambia
                print('True')
                recurso.foto = request.FILES.get('foto', 'images/recursos/None/no-img.jpg')
             
            date = datetime.strptime(request.POST.get('fecha_ingreso'), "%Y-%m-%d").date()
            recurso.fecha_ingreso = date
            recurso.caracteristicas = formRecurso.data['caracteristicas'].upper()
            recurso.tipo = formRecurso.data['tipo']
            recurso.save()
            
            return redirect('/inventario/Inventario/recursos/detail/' + str(recurso.id))
        return render(request, 'Recurso/recurso_editar.html', {'formRecurso':formRecurso, 'recurso': recurso})
    except recursos.DoesNotExist:
        messages.info(request, 'Ud. no tiene permisos para visualizar estos datos.')
        return redirect('/inventario/')

def recursosEliminarView(request):
    if request.method == 'GET':
        print('Eliminando recurso')
        idRecurso = request.GET['idRecurso']
        respuesta = request.GET['respuesta']
        
        #buscamos el proyecto al cual se encuentra asignado el recurso actualmente
        recursoAsignadoAProyecto = Recurso_Proyecto.objects.filter(idRecurso = idRecurso, estado='ACTIVO')
        #print(recursoAsignadoAProyecto)
        #buscamos el recurso al cual se encuentra asignado el rcurso actualmente
        miembroAsignadoARecurso = MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto= recursoAsignadoAProyecto[0].id, estado='ACTIVO')
        
        if respuesta == '1':
            mensaje= 'El recurso esta asignado al'
            if recursoAsignadoAProyecto.exists():            
                mensaje2=' proyecto: '+ recursoAsignadoAProyecto[0].idProyecto.nombre
                mensaje = mensaje + mensaje2 
            if miembroAsignadoARecurso.exists():
                mensaje3= ', miembro: '+ miembroAsignadoARecurso[0].idMiembro_Proyecto.idMiembro.nombre
                mensaje = mensaje + mensaje3
            return JsonResponse({ 'resultado' : mensaje +'\n ¿Esá seguro que desea continuar con la eliminación?'})
        else:
            recursoEliminado= recursos.objects.get(id=idRecurso)
            recursoEliminado.estado='INACTIVO'
            recursoEliminado.save()
            
            print('entra al miembros')
            if miembroAsignadoARecurso.exists():
                temporal0= miembroAsignadoARecurso[0]
                temporal0.estado='INACTIVO'
                temporal0.observacion='Se ha quitado el recurso al miembro por eliminación de recurso'
                temporal0.fecha= datetime.now().date()
                temporal0.save()
                
            if recursoAsignadoAProyecto.exists():
                print('entra al proyectos')
                print('Id recurso'+idRecurso)
                print('recurso proyecto'+str(recursoAsignadoAProyecto[0].id))
                proyectoCitesoft = Proyectos.objects.get(nombre = 'CITESOFT')
                temporal = recursoAsignadoAProyecto[0]
                temporal.idProyecto=proyectoCitesoft
                temporal.estado='INACTIVO'
                temporal.descripcion='El recurso ha sido eliminado'
                temporal.fecha_recurso_proyecto=datetime.now().date()
                temporal.save()
                print('guarda')
            
            return JsonResponse({ 'resultado' : 'el recurso se ha eliminado exitosamente'})
    
def listar_proyectos(request):
    proyectos = Proyectos.objects.filter(estado='ACTIVO').order_by('id')
    if request.method == 'POST':
        form = buscarProyectosForm(request.POST)
        data = form.data
        nombre = data['nombre']
               
        proyectoEsp = Proyectos.objects.filter(Q(nombre__contains=nombre.upper()) | Q(descripcion__contains=nombre.upper()) )
        # recursoEsp1={'recursoEsp1':recursoEsp}
        
        contexto = {'proyectos':proyectos,
                    'proyectoEsp':proyectoEsp
                    }
        ## print(contexto)
        return render(request, 'Proyecto/listar.html', contexto)
    else:
        contexto = {'proyectos':proyectos}
    return render(request, 'Proyecto/listar.html', contexto)

class recursosListView(ListView):
    model = recursos
    template_name = 'Inventario/recursos_list.html'

class recursosCreateView(CreateView):
    model = recursos
    form_class = recursosForm

class recursosUpdateView(UpdateView):
    model = recursos
    form_class = recursosForm


class MiembrosListView(ListView):
    model = Miembros


class MiembrosCreateView(CreateView):
    model = Miembros
    form_class = MiembrosForm

def MiembroRegistrar(request):
    if request.method == 'POST':
        formMiembro = MiembrosRegistro(request.POST, request.FILES)
        if (formMiembro.is_valid()):
            data = formMiembro.data
            print(request.FILES.get('fotoMiembro'))
            
            ## Generando nueva contraseña aleatoria
            passwordNuev = ''.join(random.choice('0123456789ABCDEF') for i in range(10))
            passwordNuevo = make_password(passwordNuev)
            
            usuarioNuevo = User(first_name= data['nombre'].upper(), 
                                last_name= data['apellido'].upper(), 
                                username= data['dni'], 
                                email= data['correo'],
                                password = passwordNuevo)
            
            ## Verificando que no se registre el mismo email 2 veces y que el DNI tenga 8 caracteres
            emailComprobacion = User.objects.filter(email = data['correo']).exists()
            
            if (emailComprobacion):
                    messages.info(request, 'El correo electrónico ingresado ya se encuentra registrado.')
            else:
                if (re.match('[0-9]{8}', data['dni'])):
                    if len(data['dni']) == 8:
                    
                        ## Intentando guardar usuario, en caso de que no esté registrado el DNI
                        try:
                            usuarioNuevo.save()
                            print('Usuario guardado')
                            
                            ## Guardando Miembro
                            miembroNuevo = Miembros(user=usuarioNuevo,
                                                   nombre=data['nombre'].upper(),
                                                   apellido=data['apellido'].upper(),
                                                   dni=data['dni'],
                                                   telefono=data['telefono'],
                                                   correo=data['correo'],
                                                   fecha_ingreso = data['fecha_ingreso'],
                                                   foto = request.FILES.get('fotoMiembro', 'images/miembros/None/no-img.jpg'),
                                                   aleatorio = ''.join(random.choice('0123456789ABCDEF') for i in range(20)),
                                                   estado_miembro = 'ACTIVO')
                            miembroNuevo.save()
                            print('Miembro guardado')
                            
                            ## Agregando a grupo Miembro
                            grupo = Group.objects.get(name='miembro_grupo')
                            grupo.user_set.add(usuarioNuevo)
                            print('Agregado al grupo')
                            
                            ## Agregando a proyecto Citesoft 
                            proyectoCitesoft = Proyectos.objects.get(nombre = 'CITESOFT')
                            cargo = Cargos.objects.get(descripcion='PERSONAL DE APOYO')
                            registrarMiembroCitesoft = Miembro_Proyecto(descripcion = 'Inició en el proyecto',
                                                                        fecha_miembro_proyecto = formMiembro.data['fecha_ingreso'],
                                                                        estado_miembro_proyecto = 'ACTIVO',
                                                                        idCargo = cargo,
                                                                        idMiembro = miembroNuevo,
                                                                        idProyecto = proyectoCitesoft
                                                                        )
                            registrarMiembroCitesoft.save()
                            print('Agregado al Citesoft')
                            
                            ## Enviar password al correo registrado
                            site_name = RequestSite(request).domain
                            print(site_name)
                            subject, from_email, to = 'Solicitud CiTeSoft', 'CiTeSoft', data['correo']
                            text_content = 'MENSAJE IMPORTANTE'
                            html_content = '<h2>Su cuenta ha sido registrada exitosamente.</h2> <p>Para iniciar sesión utilice los siguientes datos: </p><p>Usuario: '+ data['dni']+'</p><p>Contraseña: '+ passwordNuev+'</p><p>Para iniciar sesión presione <a href=http://'+ site_name +'/inventario/>aquí</a>.' 
                            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
                            
                            messages.info(request, 'El nuevo miembro ha sido registrado con éxito. Ingrese con su DNI y la siguiente contraseña: ' + passwordNuev)

                            cadena = '/inventario/Inventario/miembros/listar'
                            return redirect(cadena)
                        
                        except IntegrityError:
                            messages.info(request, 'EL DNI ingresado ya se encuentra registrado.')
                    else:
                        messages.info(request, 'EL DNI ingresado no es válido.')
                else:
                    messages.info(request, 'EL DNI ingresado no es válido.')
        else:
            print('Datos inválidos')
    else:
        formMiembro = MiembrosRegistro
    return render(request, 'Miembro/miembros_form.html', {'formMiembro': formMiembro})

def miembroEditarView(request, idMiembro):
    try:
        miembro = Miembros.objects.get(id=idMiembro)
        if request.method == 'GET':
            formMiembro = MiembrosEditForm(instance = miembro)
        else:
            formMiembro = MiembrosEditForm(request.POST, request.FILES, instance=miembro)
            print(request.FILES.get('foto'))
            miembro.nombre = formMiembro.data['nombre']
            miembro.apellido = formMiembro.data['apellido']
            #fecha nacimiento
            date1 = datetime.strptime(request.POST.get('fecha_nacimiento'), "%Y-%m-%d").date()
            miembro.fecha_nacimiento = date1
            miembro.dni = formMiembro.data['dni']
            miembro.telefono = formMiembro.data['telefono']
            miembro.correo = formMiembro.data['correo']
            #fecha ingreso
            date2 = datetime.strptime(request.POST.get('fecha_ingreso'), "%Y-%m-%d").date()
            miembro.fecha_ingreso = date2
            miembro.grado_academico = formMiembro.data['grado_academico']
            miembro.foto = request.FILES['foto'] if 'foto' in request.FILES else miembro.foto
            miembro.save()
            
            ## Editamos además los datos del usuario relacionado
            usuarioEditar = miembro.user
            usuarioEditar.username = formMiembro.data['dni']
            usuarioEditar.first_name = formMiembro.data['nombre']
            usuarioEditar.last_name = formMiembro.data['apellido']
            usuarioEditar.email = formMiembro.data['correo']
            
            usuarioEditar.save()
            
            ## redirect 18
            ## cadena = 'Inventario/recursos/detail/' + str(recurso.id) + '/'
            return redirect('/inventario/Inventario/miembros/detail/' + str(miembro.id))
        return render(request, 'Miembro/miembros_editar.html', {'formMiembro':formMiembro, 'miembro': miembro})
    except Proyectos.DoesNotExist:
        messages.info(request, 'Ud. no tiene permisos para visualizar estos datos.')
        return redirect('/inventario/')

class MiembrosDetailView(DetailView):
    model = Miembros

def detalleMiembro(request, idMiembro):
    try:
        miembro = Miembros.objects.get(id=idMiembro)
        print(idMiembro)
        proyectos = Miembro_Proyecto.objects.filter(idMiembro=idMiembro).order_by('created')
        print(proyectos)
        contexto = {'proyectos' : proyectos, 'miembro' : miembro}
        return render(request, 'Miembro/miembro_detalle.html', contexto)
    except Miembros.DoesNotExist:
        miembro = None
        contexto = {'miembro' : miembro }
        return render(request, 'Miembro/miembro_detalle.html', contexto)
    
def miembrosListarView(request):
    print('Listando miembros')
    if request.method == 'POST':
        form = buscarMiembrosForm(request.POST)
        data = form.data
        nombre = data['nombre']
               
        miembroEsp = Miembros.objects.filter(Q(nombre__contains=nombre.upper()) | Q(apellido__contains=nombre.upper()))
        miembroEsp = miembroEsp.filter(estado_miembro='ACTIVO')
        print(miembroEsp)
        
        miembros = Miembros.objects.filter(estado_miembro='ACTIVO').order_by('-fecha_nacimiento')
        contexto = {'miembros':miembros,
                    'miembrosEsp1':miembroEsp
                    }
        ## print(contexto)
        return render(request, 'Miembro/miembros.html', contexto)
    else:
        miembros = Miembros.objects.filter(estado_miembro='ACTIVO')
        contexto = {'miembros':miembros}
    return render(request, 'Miembro/miembros.html', contexto)

class MiembrosUpdateView(UpdateView):
    model = Miembros
    form_class = MiembrosForm


class Historial_RecursosListView(ListView):
    model = Historial_Recursos


class Historial_RecursosCreateView(CreateView):
    model = Historial_Recursos
    form_class = Historial_RecursosForm


class Historial_RecursosDetailView(DetailView):
    model = Historial_Recursos


class Historial_RecursosUpdateView(UpdateView):
    model = Historial_Recursos
    form_class = Historial_RecursosForm


class EstadoRecursoListView(ListView):
    model = EstadoRecurso

def detalleRecurso(request, idRecurso):
    try:
        recurso = recursos.objects.get(id=idRecurso)
        proyectoDelRecurso = Recurso_Proyecto.objects.get(idRecurso=recurso, estado='ACTIVO')
        personalACargo= MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto=proyectoDelRecurso, estado='PRESTADO')
        
        documentos = Recurso_Documento.objects.filter(idRecurso = idRecurso)

        if (personalACargo.exists()):
            contexto = {'recurso' : recurso, 'proyectoDelRecurso': proyectoDelRecurso, 'documentos': documentos, 'personaACargo': personalACargo[0]}
        else:
            contexto = {'recurso' : recurso, 'proyectoDelRecurso': proyectoDelRecurso, 'documentos': documentos }

        return render(request, 'Recurso/recurso_detalle.html', contexto)
    except (recursos.DoesNotExist, Recurso_Proyecto.DoesNotExist):
        recurso = None
        contexto = {'recurso' : recurso}
        return render(request, 'Recurso/recurso_detalle.html', contexto)

def proyectoEditarView(request, idProyecto):
    try:
        proyecto = Proyectos.objects.get(id=idProyecto)
        if request.method == 'GET':
            formProyecto = ProyectosEditForm(instance = proyecto)
        else:
            formProyecto= ProyectosEditForm(request.POST, request.FILES, instance=proyecto)
            print(request.FILES.get('foto'))
            proyecto.nombre = formProyecto.data['nombre']
            proyecto.descripcion = formProyecto.data['descripcion']
            
            if (request.FILES.get('foto', False)): ##  Si recibe una foto en el formulario la cambia
                print('True')
                proyecto.foto = request.FILES.get('foto', 'images/recursos/None/no-img.jpg')
                
            date = datetime.strptime(request.POST.get('fecha_inicio'), "%Y-%m-%d").date()
            proyecto.fecha_inicio = date
            proyecto.save()
            
            ## redirect 18
            ## cadena = 'Inventario/recursos/detail/' + str(recurso.id) + '/'
            return redirect('/inventario/Inventario/proyectos/detalle/' + str(proyecto.id))
        print(proyecto.fecha_inicio)
        fecha=proyecto.fecha_inicio
        return render(request, 'Proyecto/proyectos_editar.html', {'formProyecto':formProyecto, 'proyecto': proyecto, 'fecha': fecha})
    except Proyectos.DoesNotExist:
        messages.info(request, 'Ud. no tiene permisos para visualizar estos datos.')
        return redirect('/inventario/')

class EstadoRecursoCreateView(CreateView):
    model = EstadoRecurso
    form_class = EstadoRecursoForm


class EstadoRecursoDetailView(DetailView):
    model = EstadoRecurso


class EstadoRecursoUpdateView(UpdateView):
    model = EstadoRecurso
    form_class = EstadoRecursoForm


class EntidadListView(ListView):
    model = Entidad


class EntidadCreateView(CreateView):
    model = Entidad
    form_class = EntidadForm


class EntidadDetailView(DetailView):
    model = Entidad


class EntidadUpdateView(UpdateView):
    model = Entidad
    form_class = EntidadForm


class DocumentoListView(ListView):
    model = Documento

    def get_queryset(self):
        return Documento.objects.filter(estado='ACTIVO').order_by('id')


class DocumentoCreateView(CreateView):
    model = Documento
    form_class = DocumentoForm


class DocumentoDetailView(DetailView):
    model = Documento


class DocumentoUpdateView(UpdateView):
    model = Documento
    form_class = DocumentoForm


class CargosListView(ListView):
    model = Cargos

class CargosCreateView(CreateView):
    model = Cargos
    form_class = CargosForm


class CargosDetailView(DetailView):
    model = Cargos


class CargosUpdateView(UpdateView):
    model = Cargos
    form_class = CargosForm


class ProyectosListView(ListView):
    model = Proyectos

    def get_queryset(self):
        return Proyectos.objects.all().order_by('id')


class ProyectosCreateView(CreateView):
    model = Proyectos
    form_class = ProyectosForm


class ProyectosDetailView(DetailView):
    model = Proyectos


class ProyectosUpdateView(UpdateView):
    model = Proyectos
    form_class = ProyectosForm


class Historial_ProyectoListView(ListView):
    model = Historial_Proyecto


class Historial_ProyectoCreateView(CreateView):
    model = Historial_Proyecto
    form_class = Historial_ProyectoForm


class Historial_ProyectoDetailView(DetailView):
    model = Historial_Proyecto


class Historial_ProyectoUpdateView(UpdateView):
    model = Historial_Proyecto
    form_class = Historial_ProyectoForm


class EstadoProyectoListView(ListView):
    model = EstadoProyecto


class EstadoProyectoCreateView(CreateView):
    model = EstadoProyecto
    form_class = EstadoProyectoForm


class EstadoProyectoDetailView(DetailView):
    model = EstadoProyecto


class EstadoProyectoUpdateView(UpdateView):
    model = EstadoProyecto
    form_class = EstadoProyectoForm


class ResultadoProyectoListView(ListView):
    model = ResultadoProyecto


class ResultadoProyectoCreateView(CreateView):
    model = ResultadoProyecto
    form_class = ResultadoProyectoForm


class ResultadoProyectoDetailView(DetailView):
    model = ResultadoProyecto


class ResultadoProyectoUpdateView(UpdateView):
    model = ResultadoProyecto
    form_class = ResultadoProyectoForm


class Recurso_DocumentoListView(ListView):
    model = Recurso_Documento


class Recurso_DocumentoCreateView(CreateView):
    model = Recurso_Documento
    form_class = Recurso_DocumentoForm


class Recurso_DocumentoDetailView(DetailView):
    model = Recurso_Documento


class Recurso_DocumentoUpdateView(UpdateView):
    model = Recurso_Documento
    form_class = Recurso_DocumentoForm

class Miembro_ProyectoListView(ListView):
    model = Miembro_Proyecto

class Miembro_ProyectoCreateView(CreateView):
    model = Miembro_Proyecto
    form_class = Miembro_ProyectoForm

class Miembro_ProyectoDetailView(DetailView):
    model = Miembro_Proyecto
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs.get('object')
        context['recursosAsignados'] = MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto=id)
        return context

def Miembro_ProyectoDetail(request, idMiembroProyecto):
    try:
        miembroProyecto = Miembro_Proyecto.objects.get(id=idMiembroProyecto)
        recursosAsignados = MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto=idMiembroProyecto, estado='PRESTADO')
        contexto = {'object': miembroProyecto, 'recursosAsignados' : recursosAsignados}
        return render(request, 'Inventario/miembro_proyecto_detail.html', contexto)
    except Miembro_Proyecto.DoesNotExist:
        miembroProyecto = None
        recursosAsignados = None
        contexto = {'object': miembroProyecto, 'recursosAsignados' : recursosAsignados}
        return render(request, 'Inventario/miembro_proyecto_detail.html', contexto)

class Miembro_ProyectoUpdateView(UpdateView):
    model = Miembro_Proyecto
    form_class = Miembro_ProyectoForm

class Recurso_ProyectoListView(ListView):
    model = Recurso_Proyecto

class Recurso_ProyectoCreateView(CreateView):
    model = Recurso_Proyecto
    form_class = Recurso_ProyectoForm

class Recurso_ProyectoDetailView(DetailView):
    model = Recurso_Proyecto

class Recurso_ProyectoUpdateView(UpdateView):
    model = Recurso_Proyecto
    form_class = Recurso_ProyectoForm

class MiembroProyecto_RecursoProyectoListView(ListView):
    model = MiembroProyecto_RecursoProyecto

class MiembroProyecto_RecursoProyectoCreateView(CreateView):
    model = MiembroProyecto_RecursoProyecto
    form_class = MiembroProyecto_RecursoProyectoForm
    template = 'AsignarRecurso/recurso_miembro.html'

def gestionar_prestamos(request):
    prestamos_all = MiembroProyecto_RecursoProyecto.objects.all()
    recursos_solicitados = MiembroProyecto_RecursoProyecto.objects.filter(estado='SOLICITADO')
    recursos_prestados = MiembroProyecto_RecursoProyecto.objects.filter(estado='PRESTADO')
    recursos_devueltos = MiembroProyecto_RecursoProyecto.objects.filter(estado='DEVUELTO')
    recursos_denegados = MiembroProyecto_RecursoProyecto.objects.filter(estado='DENEGADO')

    contexto = {'recursos_solicitados': recursos_solicitados, 
                'recursos_prestados': recursos_prestados, 
                'recursos_devueltos': recursos_devueltos,
                'recursos_denegados': recursos_denegados}
    return render(request, 'Usuario/prestamos_admin.html', contexto)

def aceptarSolicitudPrestamo(request):
    if request.method == 'GET':
        idPrestamo = request.GET['idPrestamo']
        respuesta = request.GET['respuesta']

        if respuesta == '1':
            logging.info('Entra a respuesta 1 en aceptarSolicitudPrestamo')
            solicitud_por_aceptar = MiembroProyecto_RecursoProyecto.objects.get(id=idPrestamo)
            if solicitud_por_aceptar.estado == 'PRESTADO':
                return JsonResponse({'resultado': 'El recurso ya fue prestado.'})
            elif solicitud_por_aceptar.estado != 'SOLICITADO':
                return JsonResponse({'resultado': 'El recurso ya no está solicitado.'})
            return JsonResponse({'resultado': 'El recurso será PRESTADO'})
        else:
            logging.info('Entra a respuesta 2 en aceptarSolicitudPrestamo')
            solicitud_por_aceptar = MiembroProyecto_RecursoProyecto.objects.get(id=idPrestamo)
            solicitud_por_aceptar.estado = 'PRESTADO'
            logging.info('medio de respuesta')
            solicitud_por_aceptar.observacion = solicitud_por_aceptar.observacion + '\nSolicitud aceptada por el admin.'
            solicitud_por_aceptar.save() ## La solicitud ya fu aceptada

            ## Si es que se presta un recurso a un miembro, se debe denegar todos los prestamos hechos por otros usuarios que solicitan dicho recurso en especifico
            denegarTodosPrestamos(idPrestamo)

            return redirect('/inventario/gestionarPrestamos/')

        logging.info('ERROR en if or else at aceptarSolicitudPrestamo function')
        return redirect('/inventario/')

def rechazarSolicitudPrestamo(request):
    if request.method == 'GET':
        idPrestamo = request.GET['idPrestamo']
        respuesta = request.GET['respuesta']

        if respuesta == '1':
            solicitud_por_rechazar = MiembroProyecto_RecursoProyecto.objects.get(id=idPrestamo)
            if solicitud_por_rechazar != 'SOLICITADO':
                return JsonResponse({'resultado': 'El recurso ya no está solicitado.'})
            return JsonResponse({'resultado': 'El préstamo será denegado'})
        else:
            solicitud_por_rechazar = MiembroProyecto_RecursoProyecto.objects.get(id=idPrestamo)
            solicitud_por_rechazar.estado = 'DENEGADO'
            solicitud_por_rechazar.observacion = solicitud_por_rechazar.observacion + '\nSolicitud denegada por el admin.'
            solicitud_por_rechazar.save()
            return redirect('/inventario/gestionarPrestamos/')
        logging.info('ERROR en if or else at rechazarSolicitudPrestamo function')
        return redirect('/inventario/')

def denegarTodosPrestamos(idPrestamo):
    recurso_de_prestamo_realizado = MiembroProyecto_RecursoProyecto.get(id=idPrestamo).idRecurso_Proyecto
    prestamos_mismo_recurso_estado_solicitado = MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto=recurso_de_prestamo_realizado, estado='SOLICITADO')
    for iter_prestamo in prestamos_mismo_recurso_estado_solicitado:
        iter_prestamo.estado = 'DENEGADO'
        iter_prestamo.observacion = iter_prestamo.observacion + '\nEl recurso fue asignado a otro miembro.'
        iter_prestamo.save()
    
    ## TESTEAR: Desde diferentes cuentas que soliciten un mismo recurso y que al aceptar a uno de ellos, se deniegue a los demas usuarios el prestamo de dicho recurso

def asignarRecursoAMiembro(request, idProyecto, idMiembroProyecto):
    miembro = Miembro_Proyecto.objects.get(id=idMiembroProyecto)
    if request.method == 'POST':
        print(idMiembroProyecto)
        form = MiembroProyecto_RecursoProyectoForm(request.POST)
        data = form.data
        
        recursoProyecto = Recurso_Proyecto.objects.get(id=data['idRecurso_Proyecto'])
        
        miembroproyecto_recursoproyecto=  MiembroProyecto_RecursoProyecto(idMiembro_Proyecto=miembro, 
                                                                          idRecurso_Proyecto=recursoProyecto,
                                                                          observacion = 'El recurso fue asignado.',
                                                                          estado = 'PRESTADO')
        
        miembroproyecto_recursoproyecto.save()
        cadena = '/inventario/Inventario/proyectos/detalle/' + idProyecto  + '/'
        return redirect(cadena)
        
    else:
        form = MiembroProyecto_RecursoProyectoForm()
        
        ## Búsqueda de recursos en proyectos activos
        recursosProyectosActivos = Recurso_Proyecto.objects.filter(estado='ACTIVO')
        
        ## Búsqueda de recursos no asignados
        recursosNoAsignados = []
        for rPA in recursosProyectosActivos:
            if not MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto = rPA, estado='PRESTADO').exists():
                recursosNoAsignados.append(rPA)
                
        ## print(recursosNoAsignados)
        
        ## Enviando id Miembro de Proyecto      
        
               
    return render(request, 'AsignarRecurso/recurso_miembro.html', {'form': form, 'recursosNoAsignados': recursosNoAsignados, 'miembro':miembro})

def desasignarRecursoMiembro(request):
    if request.method == 'GET':
        idMiembro_Proyecto = request.GET['idMiembro_Proyecto']
        idRecurso_Proyecto = request.GET['idRecurso_Proyecto']
        
        print(idRecurso_Proyecto)
        print('-------------------')
        ## Buscamos el registro para "ELIMINARLO" (cambiarle estado)
        miembroproyecto_recursoProyecto = MiembroProyecto_RecursoProyecto.objects.get(idMiembro_Proyecto = idMiembro_Proyecto, idRecurso_Proyecto = idRecurso_Proyecto, estado='PRESTADO')
        miembroproyecto_recursoProyecto.estado = 'DEVUELTO'
        miembroproyecto_recursoProyecto.observacion = 'Se le ha quitado el recurso al miembro'
        miembroproyecto_recursoProyecto.fecha = datetime.now().date()
        miembroproyecto_recursoProyecto.save()
        
        print('El recurso ha sido desasignado.')
        
        return JsonResponse({ 'resultado' : 'El recurso ha sido desasignado.' })
    
def desasignarRecursoProyecto(request):
    if request.method == 'GET':
        print('Desasignar recurso proyecto')
        idRecurso_Proyecto = request.GET['idRecurso_Proyecto']
        respuesta = request.GET['respuesta']
        idProyecto = request.GET['idProyecto']
        print(respuesta)
        print(idRecurso_Proyecto)
        print('-------------------')
        
        miembroproyecto_recursoProyecto = MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto = idRecurso_Proyecto, estado='ACTIVO')
        
        
        if respuesta == '1':
            if miembroproyecto_recursoProyecto.exists():
                nombrePersonaACargo = miembroproyecto_recursoProyecto[0].idMiembro_Proyecto.idMiembro
                print('El recurso está asignado a ' + str(nombrePersonaACargo))
                return JsonResponse({ 'resultado' : 'El recurso está asignado a ' + str(nombrePersonaACargo) + '\n ¿Esá seguro que desea continuar con la eliminación?'})
            else:
                print('El recurso no está asignado actualmente y será asignado al proyecto principal.')
                return JsonResponse({ 'resultado' : 'El recurso será asignado al proyecto principal.' })
        
        else: ## Aquí se hacen los cambios
            print('ELIMINAAAAAAAAAAAAAAAAAAAAAR')
            if miembroproyecto_recursoProyecto.exists():
                ## Desasignando recurso al miembro
                miembroDesasignar =  miembroproyecto_recursoProyecto[0]
                miembroDesasignar.estado = 'INACTIVO'
                miembroDesasignar.observacion = 'Se le ha quitado el recurso al miembro por eliminación del recurso.'
                miembroDesasignar.fecha = datetime.now().date()
                miembroDesasignar.save()
                print('Desasignado.')
            
            ## Eliminar recurso del proyecto
            recursoProyectoEliminar = Recurso_Proyecto.objects.get(id=idRecurso_Proyecto)
            recursoProyectoEliminar.descripcion = 'El recurso ha sido eliminado del proyecto.'
            recursoProyectoEliminar.estado = 'INACTIVO'
            recursoProyectoEliminar.save()
            
            print('Eliminado del proyecto')
            
            ## Asignar recurso al proyecto CItesoft
            ## Buscar recurso en citesoft y pasarlo a activo
            proyectoCiTeSoft = Proyectos.objects.filter(nombre__iexact='citesoft')[0]
            recurso = recursos.objects.get(id = recursoProyectoEliminar.idRecurso.id)
            actualizarRecursoCitesoft = Recurso_Proyecto.objects.get(idProyecto = proyectoCiTeSoft, idRecurso = recurso)
            actualizarRecursoCitesoft.estado = 'ACTIVO'
            actualizarRecursoCitesoft.DESCRIPCION = 'Se asignó el recurso a Citesoft después de ser eliminado del proyecto ' + recursoProyectoEliminar.idProyecto.nombre
            actualizarRecursoCitesoft.fecha_recurso_proyecto = datetime.now().date()
            actualizarRecursoCitesoft.save()
            
            print('Asignado a Citesoft.')
            
            return redirect('/inventario/Inventario/proyectos/detalle/'+ idProyecto +'/')
    else:
        print('llega aquí')
        
def desasignarMiembroProyecto(request):
    if request.method == 'GET':
        print('Desasignar miembro proyecto')
        idMiembro_Proyecto = request.GET['idMiembro_Proyecto']
        respuesta = request.GET['respuesta']
        idProyecto = request.GET['idProyecto']
        miembroproyecto_recursoProyecto = MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto = idMiembro_Proyecto, estado='ACTIVO')
        #recursosAsignadosAlProyecto = MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto = idMiembro_Proyecto, estado='ACTIVO')
        #print(recursosAsignadosAlProyecto)      
        lista=' '         
        if respuesta == '1':
            if miembroproyecto_recursoProyecto.exists():
                for listado in miembroproyecto_recursoProyecto:
                    lista = lista + str(listado.idRecurso_Proyecto.idRecurso.nombre)+' '
                    
                return JsonResponse({ 'resultado' : 'El miembro tiene asignado los siguientes recursos' + lista + '\n ¿Esá seguro que desea continuar con la eliminación?'})
            else:
                return JsonResponse({ 'resultado' : 'El miembro será asignado al proyecto principal' })
        
        else: ## Aquí se hacen los cambios
            if miembroproyecto_recursoProyecto.exists():
                ## Desasignando recursos al miembro
                for recursoADesasignar in miembroproyecto_recursoProyecto:
                    recursoADesasignar.estado = 'INACTIVO' 
                    recursoADesasignar.observacion = 'Se le ha quitado el recurso al miembro por eliminación del miembro.'
                    recursoADesasignar.fecha = datetime.now().date()
                    recursoADesasignar.save()                            
            ## Eliminar miembro del proyecto
            miembroProyectoEliminar = Miembro_Proyecto.objects.get(id=idMiembro_Proyecto)
            miembroProyectoEliminar.descripcion = 'El miembro ha sido eliminado del proyecto.'
            miembroProyectoEliminar.estado_miembro_proyecto = 'INACTIVO'
            miembroProyectoEliminar.save()
            ## Asignar miembro al proyecto CItesoft
            ## Buscar recurso en citesoft y pasarlo a activo
            proyectoCiTeSoft = Proyectos.objects.filter(nombre__iexact='citesoft')[0]
            miembro = Miembros.objects.get(id = miembroProyectoEliminar.idMiembro.id)
            actualizarMiembroCitesoft = Miembro_Proyecto.objects.get(idProyecto = proyectoCiTeSoft, idMiembro = miembro)
            actualizarMiembroCitesoft.estado_miembro_proyecto = 'ACTIVO'
            actualizarMiembroCitesoft.DESCRIPCION = 'Se asignó el miembro a Citesoft después de ser eliminado del proyecto ' + miembroProyectoEliminar.idProyecto.nombre
            actualizarMiembroCitesoft.fecha_miembro_proyecto = datetime.now().date()
            actualizarMiembroCitesoft.save()
                      
            return redirect('/inventario/Inventario/proyectos/detalle/'+ idProyecto +'/')
    
class MiembroProyecto_RecursoProyectoDetailView(DetailView):
    model = MiembroProyecto_RecursoProyecto


class MiembroProyecto_RecursoProyectoUpdateView(UpdateView):
    model = MiembroProyecto_RecursoProyecto
    form_class = MiembroProyecto_RecursoProyectoForm
    
## Nuevoooooooooooooo
def miembrosEliminarView(request):
    if request.method == 'GET':
        idMiembro = request.GET['idMiembro']
        respuesta = request.GET['respuesta']
        mensaje1 = 'Proyectos: '
        mensaje2 = 'Recursos: '
        
        MiembroProyecto = Miembro_Proyecto.objects.filter(idMiembro=idMiembro, estado_miembro_proyecto='ACTIVO')        
        #RecursoProyecto = MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto = MiembroProyecto)
        #Los proyectos a los cuales pertenece el miembro
        RecursosProyecto=[]
        if respuesta == '1':
            if(MiembroProyecto.exists()):
                print('Está asignado a algun proyecto')
                for miembroproyecto in MiembroProyecto:                    
                    #obtenemos todos los recursos por asignados al miembro
                    rr= MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto = miembroproyecto, estado='ACTIVO')
                    if(rr.exists()):
                        for r in rr:
                            RecursosProyecto.append(r.idRecurso_Proyecto.idRecurso)
                            mensaje2 = mensaje2 + r.idRecurso_Proyecto.idRecurso.nombre + ' , ' 
                    mensaje1= mensaje1 + miembroproyecto.idProyecto.nombre
                return JsonResponse({ 'resultado' :'El miembro tiene asignado lo siguiente: \n'+ mensaje1 +'\n'+ mensaje2 +'\n ¿Esá seguro que desea continuar con la eliminación?'})
        else:
            if(MiembroProyecto.exists()):
                print('Está asignado a algun proyecto')
                for miembroproyecto in MiembroProyecto:                    
                    #obtenemos todos los recursos por asignados al miembro
                    rr= MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto = miembroproyecto , estado= 'ACTIVO')
                    miembroproyecto.estado_miembro_proyecto='INACTIVO'
                    miembroproyecto.descripcion='El miembro ya no es parte del proyecto debido a que fue eliminado'
                    miembroproyecto.fecha= datetime.now().date()  
                    miembroproyecto.save()              
                    if(rr.exists()):
                        for r in rr:
                            #RecursosProyecto.append(r.idRecurso_Proyecto.idRecurso)
                            r.estado='INACTIVO'
                            r.fecha= datetime.now().date()
                            r.observacion='El miembro ya no propietario del recurso debido a que fue eliminado'
                            r.save()
            miembroEliminado= Miembros.objects.get(id= idMiembro, estado_miembro='ACTIVO')
            miembroEliminado.estado_miembro='INACTIVO'
            miembroEliminado.save()
            return JsonResponse({ 'resultado' : 'el miembro se ha eliminado exitosamente'})

def proyectosEliminarView(request):
    if request.method == 'GET':
        idProyecto = request.GET['idProyecto']
        respuesta = request.GET['respuesta']
        ## print('entra al metodo de eliminar proyecto')
        #Obtener los miembros que tiene el proyecto, sin importar el estado, porq pueden haber sido solo desasignado
        MiembroProyecto = Miembro_Proyecto.objects.filter(idProyecto=idProyecto)
        #Obtener los recurso que tiene el proyecto, sin importar el estado, porq pueden haber sido solo desasignado
        RecursoProyecto = Recurso_Proyecto.objects.filter(idProyecto=idProyecto)
        #RecursoProyecto = MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto = MiembroProyecto)
        ProyectoEliminado= Proyectos.objects.get(id=idProyecto)
        #Los proyectos a los cuales pertenece el miembro
        if respuesta == '1':
            return JsonResponse({ 'resultado' :'El proyecto tiene asignado los recursos y miembros que se muestran en la parte inferior \n ¿Está seguro que desea continuar con la eliminación?'})
        else:
            if(MiembroProyecto.exists()):
                print('El proyecto contiene miembros')
                for miembroproyecto in MiembroProyecto:                    
                    #obtenemos todos los recursos por asignados al miembro
                    rr= MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto = miembroproyecto)
                    if(rr.exists()):
                        for r in rr:
                            r.estado='INACTIVO'
                            r.observacion='El proyecto al cual pertenecia el miembro ha sido borrado, se desasigna el recurso al miembro'
                            r.fecha=datetime.now().date()
                            r.save()
                    miembroproyecto.estado_miembro_proyecto='INACTIVO'
                    miembroproyecto.descripcion='El miembro ya no es parte del proyecto, debido a la eliminación del proyecto'
                    miembroproyecto.fecha= datetime.now().date()
                    miembroproyecto.save()
            if(RecursoProyecto.exists()):
                for recursoproyecto in RecursoProyecto:                    
                    #obtenemos todos los recursos por asignados al miembro
                    rr2= MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto = recursoproyecto)
                    if(rr2.exists()):
                        for r1 in rr2:
                            r1.estado='INACTIVO'
                            r1.observacion='El proyecto al cual pertenecia el recurso ha sido borrado, se desasigna el recurso al miembro'
                            r1.fecha=datetime.now().date()
                            r1.save()
                    recursoproyecto.estado='INACTIVO'
                    recursoproyecto.descripcion='El recurso ya no es parte del proyecto, debido a la eliminación del proyecto'
                    recursoproyecto.fecha_recurso_proyecto=datetime.now().date()
                    recursoproyecto.save() 
                                
            ProyectoEliminado.estado='INACTIVO'                        
            ProyectoEliminado.save()
            return JsonResponse({ 'resultado' : 'El proyecto se ha eliminado exitosamente'})

def Recurso_Documento_Add(request, idRecurso):
    try:
        recurso = recursos.objects.get(id=idRecurso)
        form_class = Recurso_DocumentoForm()
        contexto = {'recurso': recurso, 'form': form_class}
        
        if request.method == 'POST':
            form = Recurso_DocumentoForm(request.POST)
            
            document = Documento.objects.get(id=form.data['idDocumento'])
            
            RecursoDocumento = Recurso_Documento(idDocumento = document, idRecurso = recurso)
            RecursoDocumento.save()
            cadena = '/inventario/Inventario/recursos/detail/' + str(recurso.id) + '/'
            return redirect(cadena)
        else:
            form_class = Recurso_DocumentoForm()
            contexto = {'recurso': recurso, 'form': form_class}
        return render(request, 'Inventario/recurso_documento_form.html', contexto)
    
    
    except recursos.DoesNotExist:
        recurso = None
        contexto = {'recurso' : recurso }
        return render(request, 'Proyecto/proyecto_detalle.html', contexto)
    

def reportes(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="test01.pdf"'
    pdf_obj = canvas.Canvas(response)

    pdf_obj.drawString(100, 100, "Hello world.")
    pdf_obj.showPage()
    pdf_obj.save()
    return response

    #return render(request, 'Reportes/generar.html')


def get_recursos_tabla():
    recursos_tabla = recursos.objects.all()
    recursos_campos = [ ['Código de patrimonio', 'Es el código dado por la universidad'],
                        ['Número de producto', 'Propio de cada tipo o modelo de recurso'], 
                        ['Número de serie', 'Propio de cada recurso'],
                        ['Recurso' , 'Tipo de recurso'],
                        ['Características', 'Características del recurso'],
                        ['Imagen', 'Imagen del recurso'],
                        ['Fecha de Ingreso', 'Fecha cuando fue entregado por la universidad'],
                        ['Tipo de Recurso', 'Tangible o intangible'],
                        ['Fecha de registro', 'Fecha en que fue registrado en el sistema de inventario'],
                        ['Última actualización', 'Última fecha en que fue actualizado dicho registro']]

    return (recursos_tabla, recursos_campos)


class ReportResourcePDF(View):
    def cabecera(self, pdf):
        logo_imagen = settings.MEDIA_ROOT + 'citesoft.jpeg'
        pdf.drawImage(logo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

