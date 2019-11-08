from django.views.generic import DetailView, ListView, UpdateView, CreateView
from ..models import recursos, Miembros, Historial_Recursos, EstadoRecurso, Entidad, Documento, Cargos, Proyectos, Historial_Proyecto, EstadoProyecto, ResultadoProyecto, Recurso_Documento, Miembro_Proyecto, Recurso_Proyecto, MiembroProyecto_RecursoProyecto
from ..forms import recursosForm, MiembrosForm, Historial_RecursosForm, EstadoRecursoForm, EntidadForm, DocumentoForm, CargosForm, ProyectosForm, Historial_ProyectoForm, EstadoProyectoForm, ResultadoProyectoForm, Recurso_DocumentoForm, Miembro_ProyectoForm, Recurso_ProyectoForm, MiembroProyecto_RecursoProyectoForm, SolicitarRegistroForm
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from Inventario.forms import RegistrarProyectoForm, CoordinadorProyectoForm, \
    MiembroProyectoForm, buscarRecursosForm, UserForm, recursoEditForm, buscarProyectosForm
import re
from django.contrib.auth.models import Group, User
from django.core.mail.message import EmailMultiAlternatives
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from django.core import serializers
from django.contrib.sites.requests import RequestSite
import random
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from django.contrib.auth.views import login
from django.shortcuts import redirect
import datetime

import logging


def inicio(request):
    return render(request, 'indexMiembros.html')

def custom_login(request):
    if request.user.is_authenticated :
        return render(request, 'Inventario/index.html')
    else:
        return redirect('login')

def listarSolicitudes(request):
    solicitudes = Miembros.objects.filter(estado_miembro='PENDIENTE')
    contexto = {'solicitudes' : solicitudes }
    return render(request, 'Registro/solicitud.html', contexto)


def detalleProyecto(request, idProyecto):
    try:
        proyecto = Proyectos.objects.get(id=idProyecto)
        miembros = Miembro_Proyecto.objects.filter(idProyecto=proyecto).order_by('created')
        recursos = Recurso_Proyecto.objects.filter(idProyecto=proyecto).order_by('created')
        contexto = {'proyecto' : proyecto, 'miembros' : miembros, 'recursos': recursos}
        return render(request, 'Proyecto/proyecto_detalle_miembro.html', contexto)
    except Proyectos.DoesNotExist:
        proyecto = None
        contexto = {'proyecto' : proyecto }
        return render(request, 'Proyecto/proyecto_detalle_miembro.html', contexto)

def asignarMiembroProyecto(request, idProyecto):
    try:
        proyecto = Proyectos.objects.get(id=idProyecto)
        miembrosActivos = Miembros.objects.filter(estado_miembro='ACTIVO')
        miembros = []
        for m in miembrosActivos:
            if Miembro_Proyecto.objects.filter(idMiembro=m, idProyecto=proyecto).exists():
                continue
            else:
                miembros.append(m)
                
        if request.method == 'POST':
            form = MiembroProyectoForm(request.POST)
            if (form.is_valid()):
                date = datetime.datetime.strptime(request.POST.get('fecha_miembro_proyecto'), "%Y-%m-%d").date()
                print(date)
                MiembroProyecto = Miembro_Proyecto(descripcion=form.data['descripcion'],
                                                   idProyecto=proyecto,
                                                   idCargo=Cargos.objects.get(id=form.data['idCargo']),
                                                   fecha_miembro_proyecto= date,
                                                   idMiembro=Miembros.objects.get(id=form.data['idMiembro']),
                                                   estado_miembro_proyecto='Activo'
                                                   )
                MiembroProyecto.save()
                print(MiembroProyecto)
                cadena = '/Inventario/proyectos/detalle/' + str(proyecto.id) + '/'
                return redirect(cadena)
            else:
                print('error')
        else:
            form = MiembroProyectoForm()
        return render(request, 'Proyecto/asignar_miembro.html', {'form': form, 'proyecto':proyecto, 'miembros' : miembros })
    except Proyectos.DoesNotExist:
        return redirect('/')

def asignarRecursoProyecto(request, idProyecto):
    try:
        proyecto = Proyectos.objects.get(id=idProyecto)        
        recursosAsig = recursos.objects.filter(rn_recurso=None)
                
        if request.method == 'POST':
            form = Recurso_ProyectoForm(request.POST)
            print(form.data)                
            date = datetime.datetime.strptime(request.POST.get('fecha_recurso_proyecto'), "%Y-%m-%d").date()
            print(date)
            RecursoProyecto = Recurso_Proyecto(descripcion = 'Asignado a ' + proyecto.nombre, 
                                               estado = 'ACTIVO',
                                               fecha_recurso_proyecto = date,
                                               idProyecto = proyecto,
                                               idRecurso = recursos.objects.get(id=form.data['idRecurso']))
            RecursoProyecto.save()
            print(RecursoProyecto)
                
            cadena = '/Inventario/proyectos/detalle/' + str(proyecto.id) + '/'
            return redirect(cadena)
        else:
            form = Recurso_ProyectoForm()
        return render(request, 'Proyecto/asignar_recurso.html', {'form': form, 'proyecto':proyecto, 'recursos' : recursosAsig })
    except Proyectos.DoesNotExist:
        return redirect('/')

    
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Miembros.objects.filter(nombre=username).exists(),
        'objects' : serializers.serialize('json', Miembros.objects.filter(estado_miembro='PENDIENTE'), fields=['id', 'nombre'])
    }
    print(data)
    return JsonResponse(data)

def recursosListarView(request):
    username = request.user.username
    miembro = Miembros.objects.get(dni=username)
    proyectos_del_miembro = Miembro_Proyecto.objects.filter(idMiembro=miembro, estado_miembro_proyecto='ACTIVO')

    if request.method == 'POST':
        form = buscarRecursosForm(request.POST)
        data = form.data
        nombre = data['nombre']
               
        recursoEsp = recursos.objects.filter(Q(nombre__contains=nombre.upper()) | Q(caracteristicas__contains=nombre.upper()) )
        # recursoEsp1={'recursoEsp1':recursoEsp}
        recurso = recursos.objects.filter(estado='ACTIVO')
        estadosRecurso = []
        for r in recurso:
            recursoProyecto = Recurso_Proyecto.objects.filter(idRecurso=r)[0]
            recurso_proyectos_list = Recurso_Proyecto.objects.filter(idRecurso=r, estado='ACTIVO')
            miembro_proyectos_list = Miembro_Proyecto.objects.filter(idMiembro=miembro, estado_miembro_proyecto='ACTIVO')
            solicitado_antes_por_miembro_actual = MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto__in=recurso_proyectos_list, idMiembro_Proyecto__in=miembro_proyectos_list, estado='SOLICITADO')
            if MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto = recursoProyecto, estado='PRESTADO').exists():
                miembro_encargado = MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto=recursoProyecto, estado='PRESTADO')[0].idMiembro_Proyecto.idMiembro
                estadosRecurso.append('ASIGNADO' + str(miembro_encargado))
            elif solicitado_antes_por_miembro_actual.exists():
                estadosRecurso.append('USTED YA LO SOLICITO')
            else:
                estadosRecurso.append('SIN ASIGNAR')
        
        print(estadosRecurso)
        juntos = zip(recurso, estadosRecurso)
                   
        contexto = {'recursoss':recurso,
                    'recursoEsp1':recursoEsp,
                    'juntos': juntos,
                    'proyectos_del_miembro':proyectos_del_miembro
                    }
        ## print(contexto)
        return render(request, 'Recurso/recursosM.html', contexto)
    else:    
        recurso = recursos.objects.filter(estado='ACTIVO')
        listado = [True]
        estadosRecurso = []
        for r in recurso:
            recursoProyecto = Recurso_Proyecto.objects.filter(idRecurso=r)[0]##, estado='ACTIVO')
            recurso_proyectos_list = Recurso_Proyecto.objects.filter(idRecurso=r, estado='ACTIVO')
            miembro_proyectos_list = Miembro_Proyecto.objects.filter(idMiembro=miembro, estado_miembro_proyecto='ACTIVO')
            solicitado_antes_por_miembro_actual = MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto__in=recurso_proyectos_list, idMiembro_Proyecto__in=proyectos_del_miembro, estado='SOLICITADO')
            if MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto = recursoProyecto, estado='PRESTADO').exists():
                miembro_encargado = MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto=recursoProyecto, estado='PRESTADO')[0].idMiembro_Proyecto.idMiembro
                estadosRecurso.append('ASIGNADO A: ' + str(miembro_encargado))
            elif solicitado_antes_por_miembro_actual.exists():
                estadosRecurso.append('USTED YA LO SOLICITO')
            else:
                estadosRecurso.append('SIN ASIGNAR')
        
        print(estadosRecurso)
        juntos = zip(recurso, estadosRecurso)
        
        contexto = {'recursoss':recurso,
                    'estadosRecurso':estadosRecurso,
                    'juntos':juntos,
                    'listado':listado,
                    'proyectos_del_miembro':proyectos_del_miembro}
    return render(request, 'Recurso/recursosM.html', contexto)


'''    if request.method == 'POST':
        form = buscarRecursosForm(request.POST)
        data = form.data
        nombre = data['nombre']
               
        recursoEsp = recursos.objects.filter(Q(nombre__contains=nombre.upper()) | Q(caracteristicas__contains=nombre.upper()))
        # recursoEsp1={'recursoEsp1':recursoEsp}
        recurso = recursos.objects.all()
        contexto = {'recursoss':recurso,
                    'recursoEsp1':recursoEsp
                    }
        print(contexto)
        return render(request, 'Recurso/recursosM.html', contexto)
    else:    
        recurso = recursos.objects.all()
        contexto = {'recursoss':recurso}
    return render(request, 'Recurso/recursosM.html', contexto)'''

def detalleRecurso(request, idRecurso):
    try:
        recurso = recursos.objects.get(id=idRecurso)
        proyectoDelRecurso = Recurso_Proyecto.objects.get(idRecurso=recurso, estado='ACTIVO')
        personalACargo= MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto=proyectoDelRecurso, estado='PRESTADO')

        if (personalACargo.exists()):
            contexto = {'recurso' : recurso, 'proyectoDelRecurso': proyectoDelRecurso, 'personaACargo': personalACargo[0]}
        else:
            contexto = {'recurso' : recurso, 'proyectoDelRecurso': proyectoDelRecurso}

        return render(request, 'Recurso/recurso_detalle_miembro.html', contexto)
    except (recursos.DoesNotExist, Recurso_Proyecto.DoesNotExist):
        recurso = None
        contexto = {'recurso' : recurso}
        return render(request, 'Recurso/recurso_detalle_miembro.html', contexto)


def get_user_profile(request, username):
    miembro = Miembros.objects.get(dni=username)
    return render(request, 'Usuario/perfil.html', {"miembro":miembro})

def editar_datos_miembro(request, username):
    miembro = Miembros.objects.get(dni=username)
    otros_grados_academicos = [x[0] for x in Miembros.grados_lista if not x[0] == miembro.grado_academico]
    if request.method == 'POST':
        foto = request.FILES.get('foto', 'images/miembros/None/no-img.jpg')
        print(foto)
        print ('seguro que es este')

        dni = request.POST.get('dni')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        telefono = request.POST.get('telefono')
        grado_academico = request.POST.get('grado_academico')
        #password = request.POST.get('password')
        #password_encrypted = make_password(password)
        miembro.foto = request.FILES['foto'] if 'foto' in request.FILES else miembro.foto
        #miembro.foto = foto
        miembro.nombre = nombre
        miembro.apellido = apellido
        miembro.fecha_ingreso = fecha_ingreso
        miembro.telefono = telefono
        miembro.grado_academico = grado_academico

        #miembro.user.password = password_encrypted
        miembro.user.first_name = nombre
        miembro.user.last_name = apellido
        miembro.user.email = correo

        miembro.save()
        miembro.user.save()


        ## Cuando se cambia la contraseñad
        messages.info(request, 'Debe volver a iniciar sesión')
        return render(request, 'Usuario/perfil.html', {"miembro":miembro})
    else:
        return render(request, 'Usuario/editar_perfil.html', {"miembro":miembro, "otros_grados_academicos": otros_grados_academicos})

def editar_miembro_contras(request, username):
    miembro = Miembros.objects.get(dni=username)
    
    if request.method == 'POST':
        contra_actual = request.POST.get('contra_actual')
        contra_nueva = request.POST.get('contra_nueva')
        contra_nueva_confirma = request.POST.get('contra_nueva_confirmada')
        password_encrypted = make_password(contra_actual)

        
        if miembro.user.check_password(contra_actual): ## Comprobando password actual correcto
            if contra_nueva == contra_nueva_confirma:
                if validarContraseña(contra_nueva):
                    miembro.user.password = make_password(contra_nueva)
                    miembro.user.save()
                    # return JsonResponse({ 'resultado' : 'Contraseña cambiada exitosamente.' })
                    messages.info(request, 'Contraseña cambiada exitosamente.')
                    return render(request, 'Usuario/perfil.html', {"miembro":miembro})
                else: ## Contraseña no cumple reglas
                    messages.info(request, 'La nueva contraseña debe tener al menos 5 caracteres.')
            else: ## Mensaje de contraseña nueva no coinciden
                messages.info(request, 'Las contraseñas no coinciden.')
        else:
            messages.info(request, 'Contraseña actual incorrecta.')
        
        return render(request, 'Usuario/editar_contrasena.html', {"miembro":miembro})
    else:
        return render(request, 'Usuario/editar_contrasena.html', {"miembro":miembro})

def validarContraseña(contra_nueva):
    return len(contra_nueva) >= 5

def recursosEditarView(request, idRecurso):
    try:
        recurso = recursos.objects.get(id=idRecurso)
        if request.method == 'GET':
            formRecurso = recursoEditForm(instance=recurso)
        else:
            formRecurso= recursoEditForm(request.POST, request.FILES, instance=recurso)
            print(request.FILES.get('foto'))
            recurso.cod_patrimonio = formRecurso.data['cod_patrimonio']
            recurso.nro_producto = formRecurso.data['nro_producto']
            recurso.nro_serie = formRecurso.data['nro_serie']
            recurso.nombre = formRecurso.data['nombre']
            if (request.FILES.get('foto') is 'None'):
                print('Cambiando foto')
                recurso.foto = request.FILES.get('foto', 'images/recursos/None/no-img.jpg')
            else:
                print('No se cambia la foto')
            ## 
            date = datetime.datetime.strptime(request.POST.get('fecha_ingreso'), "%d-%m-%Y").date()
            recurso.fecha_ingreso = date
            recurso.caracteristicas = formRecurso.data['caracteristicas']
            recurso.tipo = formRecurso.data['tipo']
            recurso.save()
            
            ## redirect 18
            ## cadena = 'Inventario/recursos/detail/' + str(recurso.id) + '/'
            return redirect('/Inventario/recursos/')
        return render(request, 'Recurso/recurso_editar.html', {'formRecurso':formRecurso, 'recurso': recurso})
    except recursos.DoesNotExist:
        messages.info(request, 'Usted no tiene permisos para visualizar estos datos.')
        return redirect('/')
        
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
        return render(request, 'Proyecto/listar_miembro_vista.html', contexto)
    else:
        contexto = {'proyectos':proyectos}
    return render(request, 'Proyecto/listar_miembro_vista.html', contexto)

def prestamos_listar(request):
    '''
    Listar todos los préstamos del usuario actual (get username del user)
    '''
    username = request.user.username
    miembro = Miembros.objects.get(dni=username)
    miembro_proyecto = Miembro_Proyecto.objects.filter(idMiembro=miembro, estado_miembro_proyecto='ACTIVO')
    #prestamod_todos = MiembroProyecto_RecursoProyecto.objects.all()
    solicitudes_actuales = MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto__in=miembro_proyecto, estado='SOLICITADO')
    prestamos_actuales = MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto__in=miembro_proyecto, estado='PRESTADO')
    prestamos_pasados = MiembroProyecto_RecursoProyecto.objects.filter(idMiembro_Proyecto__in=miembro_proyecto , estado='DEVUELTO') ## Tambien pueden mostrarse los observados
    contexto = {    'miembro': miembro,
                    'solicitudes_actuales': solicitudes_actuales,
                    'prestamos_actuales': prestamos_actuales,
                    'prestamos_pasados': prestamos_pasados
                }
    return render(request, 'Usuario/prestamos.html', contexto)

def solicitarRecurso(request):
    username = request.user.username
    miembro = Miembros.objects.get(dni=username)
    if request.method == 'GET':
        logging.info('AQUI HAY INFO EXTRA')
        respuesta = request.GET['respuesta']
        idRecurso = request.GET['idRecurso']
        id_proyecto_del_miembro = request.GET['id_proyecto_del_miembro']
        ## VALIDAR QIE EL RECURSO NO ESTÉ PRESTADO ( U PERDIDO, PREGUNTAR)
        if respuesta == '1':
            recurso_proyecto = Recurso_Proyecto.objects.filter(idRecurso=idRecurso, estado='ACTIVO')[0]
            recurso_prestado = MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto=recurso_proyecto, estado='PRESTADO')
            recurso_proyectos_list = Recurso_Proyecto.objects.filter(idRecurso=idRecurso, estado='ACTIVO')
            miembro_proyectos_list = Miembro_Proyecto.objects.filter(idMiembro=miembro, estado_miembro_proyecto='ACTIVO')
            recurso_solicitado_antes_por_miembro_actual = MiembroProyecto_RecursoProyecto.objects.filter(idRecurso_Proyecto__in=recurso_proyectos_list, idMiembro_Proyecto__in=miembro_proyectos_list, estado='SOLICITADO')
            if recurso_prestado.exists():
                #msj_fallo = ''
                ## NO DEBE TENER CONFIRMACION DE MENSAJE, SOLO DEBE SER UN MENSAJE INFORMATIVO Y RECARGAR LA MISMA PAGINA...
                return JsonResponse({ 'resultado' : 'El recurso está prestado a ' + str(recurso_prestado.idMiembro_Proyecto.idMiembro) + '\nNo se le puede asignar este recurso.'})
            elif recurso_solicitado_antes_por_miembro_actual.exists():
                return JsonResponse({ 'resultado': 'Ya solicitó previamente el recurso ' + str(recurso_proyecto)})
            else:
                return JsonResponse({ 'resultado': 'Se solicitará el recurso ' + str(recurso_proyecto)})
        ## ASIGNAR O PRESTAR EL RECURSO AL MIEMBRO DE DETERMINADO PROYECTO
        else:
            miembro_proyecto = Miembro_Proyecto.objects.filter(idMiembro=miembro, idProyecto=id_proyecto_del_miembro, estado_miembro_proyecto='ACTIVO')[0]
            recurso_proyecto = Recurso_Proyecto.objects.filter(idRecurso=idRecurso, estado='ACTIVO')[0]

            solicitud_de_recurso = MiembroProyecto_RecursoProyecto( idMiembro_Proyecto = miembro_proyecto,
                                                                    idRecurso_Proyecto = recurso_proyecto,
                                                                    observacion = 'El recurso fue solicitado por '+ str(miembro_proyecto.idMiembro),
                                                                    estado='SOLICITADO')
            solicitud_de_recurso.save()
            return redirect('/inventario/')

    return redirect('/inventario/prestamos/')

class recursosListView(ListView):
    model = recursos
    template_name = 'Inventario/recursos_list.html'

class recursosCreateView(CreateView):
    model = recursos
    form_class = recursosForm


class recursosDetailView(DetailView):
    model = recursos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs.get('object')
        context['documentos'] = Recurso_Documento.objects.filter(idRecurso=id)
        return context


class recursosUpdateView(UpdateView):
    model = recursos
    form_class = recursosForm


class MiembrosListView(ListView):
    model = Miembros


class MiembrosCreateView(CreateView):
    model = Miembros
    form_class = MiembrosForm


class MiembrosDetailView(DetailView):
    model = Miembros


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


class MiembroProyecto_RecursoProyectoDetailView(DetailView):
    model = MiembroProyecto_RecursoProyecto


class MiembroProyecto_RecursoProyectoUpdateView(UpdateView):
    model = MiembroProyecto_RecursoProyecto
    form_class = MiembroProyecto_RecursoProyectoForm
