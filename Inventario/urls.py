from django.conf.urls import url, include
from rest_framework import routers
from . import api

from Inventario.views import administrador, miembro, general
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete, logout

from django.conf import settings

router = routers.DefaultRouter()
router.register(r'recursos', api.recursosViewSet)
router.register(r'miembros', api.MiembrosViewSet)
router.register(r'historial_recursos', api.Historial_RecursosViewSet)
router.register(r'estadorecurso', api.EstadoRecursoViewSet)
router.register(r'entidad', api.EntidadViewSet)
router.register(r'documento', api.DocumentoViewSet)
router.register(r'cargos', api.CargosViewSet)
router.register(r'proyectos', api.ProyectosViewSet)
router.register(r'historial_proyecto', api.Historial_ProyectoViewSet)
router.register(r'estadoproyecto', api.EstadoProyectoViewSet)
router.register(r'resultadoproyecto', api.ResultadoProyectoViewSet)
router.register(r'recurso_documento', api.Recurso_DocumentoViewSet)
router.register(r'miembro_proyecto', api.Miembro_ProyectoViewSet)
router.register(r'recurso_proyecto', api.Recurso_ProyectoViewSet)
router.register(r'miembroproyecto_recursoproyecto', api.MiembroProyecto_RecursoProyectoViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^reset/password_reset', password_reset, 
        {'template_name':'Recuperar/password_reset_form.html',
        'email_template_name': 'Recuperar/password_reset_email.html'}, 
        name='password_reset'), 
    url(r'^password_reset_done', password_reset_done, 
        {'template_name': 'Recuperar/password_reset_done.html'}, 
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, 
        {'template_name': 'Recuperar/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^reset/done', password_reset_complete, {'template_name': 'Recuperar/password_reset_complete.html'},
        name='password_reset_complete'),
)

urlpatterns += (
    # urls for recursos
    # url(r'^Inventario/recursos/$', administrador.recursosListarView, name='Inventario_recursos_list'),
    url(r'^Inventario/recursos/create/$', administrador.registrarRecursos, name='Inventario_recursos_create'),    
    url(r'^Inventario/recursos/detail/(?P<idRecurso>\S+)/$', administrador.detalleRecurso, name='Inventario_recursos_detail'),
    url(r'^Inventario/recursos/listar/', administrador.recursosListarView, name='Inventario_recursos_listar'),
    url(r'^Inventario/recursos/listaM/', miembro.recursosListarView, name='Inventario_recursos_listar_miembro'),
    url(r'^Inventario/recursos/update/(?P<idRecurso>\S+)/$', administrador.recursosEditarView, name='Inventario_recursos_update'),
    url(r'^Inventario/recursos/delete/$', administrador.recursosEliminarView, name='Inventario_miembros_delete'),
)

urlpatterns += (
    # urls for Miembros
    # url(r'^Inventario/miembros/$', administrador.MiembrosListView.as_view(), name='Inventario_miembros_list'),
    # url(r'^Inventario/miembros/create/$', administrador.MiembrosCreateView.as_view(), name='Inventario_miembros_create'),
    url(r'^Inventario/miembros/registrar/$', administrador.MiembroRegistrar, name='Inventario_miembros_registro'),
    url(r'^Inventario/miembros/detail/(?P<idMiembro>\S+)/$', administrador.detalleMiembro, name='Inventario_miembros_detail'),
    url(r'^Inventario/miembros/update/(?P<idMiembro>\S+)$', administrador.miembroEditarView, name='Inventario_miembros_update'),
    url(r'^Inventario/miembros/listar/$', administrador.miembrosListarView, name='Inventario_miembros_list'),
    url(r'^Inventario/miembros/delete/$', administrador.miembrosEliminarView, name='Inventario_miembros_delete'),
    url(r'^Inventario/miembros/registrar/(?P<idUser>\S+)/(?P<aleatorio>\S+)/$', administrador.registrarMiembro, name='Inventario_miembros_registrar'),
)

urlpatterns += (
    # urls for Historial_Recursos
    url(r'^Inventario/historial_recursos/$', administrador.Historial_RecursosListView.as_view(), name='Inventario_historial_recursos_list'),
    url(r'^Inventario/historial_recursos/create/$', administrador.Historial_RecursosCreateView.as_view(), name='Inventario_historial_recursos_create'),
    url(r'^Inventario/historial_recursos/detail/(?P<pk>\S+)/$', administrador.Historial_RecursosDetailView.as_view(), name='Inventario_historial_recursos_detail'),
    url(r'^Inventario/historial_recursos/update/(?P<pk>\S+)/$', administrador.Historial_RecursosUpdateView.as_view(), name='Inventario_historial_recursos_update'),
)

urlpatterns += (
    # urls for EstadoRecurso
    url(r'^Inventario/estadorecurso/$', administrador.EstadoRecursoListView.as_view(), name='Inventario_estadorecurso_list'),
    url(r'^Inventario/estadorecurso/create/$', administrador.EstadoRecursoCreateView.as_view(), name='Inventario_estadorecurso_create'),
    url(r'^Inventario/estadorecurso/detail/(?P<pk>\S+)/$', administrador.EstadoRecursoDetailView.as_view(), name='Inventario_estadorecurso_detail'),
    url(r'^Inventario/estadorecurso/update/(?P<pk>\S+)/$', administrador.EstadoRecursoUpdateView.as_view(), name='Inventario_estadorecurso_update'),
)

urlpatterns += (
    # urls for Entidad
    url(r'^Inventario/entidad/$', administrador.EntidadListView.as_view(), name='Inventario_entidad_list'),
    url(r'^Inventario/entidad/create/$', administrador.EntidadCreateView.as_view(), name='Inventario_entidad_create'),
    url(r'^Inventario/entidad/detail/(?P<pk>\S+)/$', administrador.EntidadDetailView.as_view(), name='Inventario_entidad_detail'),
    url(r'^Inventario/entidad/update/(?P<pk>\S+)/$', administrador.EntidadUpdateView.as_view(), name='Inventario_entidad_update'),
)

urlpatterns += (
    # urls for Documento
    url(r'^Inventario/documento/$', administrador.DocumentoListView.as_view(), name='Inventario_documento_list'),
    url(r'^Inventario/documento/create/$', administrador.DocumentoCreateView.as_view(), name='Inventario_documento_create'),
    url(r'^Inventario/documento/detail/(?P<pk>\S+)/$', administrador.DocumentoDetailView.as_view(), name='Inventario_documento_detail'),
    url(r'^Inventario/documento/update/(?P<pk>\S+)/$', administrador.DocumentoUpdateView.as_view(), name='Inventario_documento_update'),
)

urlpatterns += (
    # urls for Cargos
    url(r'^Inventario/cargos/$', administrador.CargosListView.as_view(), name='Inventario_cargos_list'),
    url(r'^Inventario/cargos/create/$', administrador.CargosCreateView.as_view(), name='Inventario_cargos_create'),
    url(r'^Inventario/cargos/detail/(?P<pk>\S+)/$', administrador.CargosDetailView.as_view(), name='Inventario_cargos_detail'),
    url(r'^Inventario/cargos/update/(?P<pk>\S+)/$', administrador.CargosUpdateView.as_view(), name='Inventario_cargos_update'),
)

urlpatterns += (
    # urls for Proyectos
    url(r'^Inventario/proyectos/$', administrador.listar_proyectos, name='Inventario_proyectos_list'),
    url(r'^Inventario/proyectos/asignar/(?P<idProyecto>\S+)/$', administrador.asignarMiembroProyecto, name='asignar_miembro_proyecto'),
    url(r'^Inventario/proyectos/asignarRsolicituecurso/(?P<idProyecto>\S+)/$', administrador.asignarRecursoProyecto, name='asignar_recurso_proyecto'),
    url(r'^ajax/validate_username/$', administrador.validate_username, name='validate_username'),
    url(r'^Inventario/proyectos/detalle/(?P<idProyecto>\S+)/$', administrador.detalleProyecto, name='Inventario_proyectos_detalle'),
    url(r'^Inventario/proyectos/create/$', administrador.registrarProyecto, name='Inventario_proyectos_create'),
    url(r'^Inventario/proyectos/listar/$', administrador.listar_proyectos, name='Inventario_proyectos_list'),
    url(r'^Inventario/proyectos/lista/$', miembro.listar_proyectos, name='Inventario_proyectos_list_miembro'),
    url(r'^Inventario/proyectos/update/(?P<idProyecto>\S+)/$', administrador.proyectoEditarView, name='Inventario_proyectos_update'),
    url(r'^Inventario/proyectos/delete/$', administrador.proyectosEliminarView, name='Inventario_proyectos_delete'),
)

urlpatterns += (
    # urls for Historial_Proyecto
    url(r'^Inventario/historial_proyecto/$', administrador.Historial_ProyectoListView.as_view(), name='Inventario_historial_proyecto_list'),
    url(r'^Inventario/historial_proyecto/create/$', administrador.Historial_ProyectoCreateView.as_view(), name='Inventario_historial_proyecto_create'),
    url(r'^Inventario/historial_proyecto/detail/(?P<pk>\S+)/$', administrador.Historial_ProyectoDetailView.as_view(), name='Inventario_historial_proyecto_detail'),
    url(r'^Inventario/historial_proyecto/update/(?P<pk>\S+)/$', administrador.Historial_ProyectoUpdateView.as_view(), name='Inventario_historial_proyecto_update'),
)

urlpatterns += (
    # urls for EstadoProyecto
    url(r'^Inventario/estadoproyecto/$', administrador.EstadoProyectoListView.as_view(), name='Inventario_estadoproyecto_list'),
    url(r'^Inventario/estadoproyecto/create/$', administrador.EstadoProyectoCreateView.as_view(), name='Inventario_estadoproyecto_create'),
    url(r'^Inventario/estadoproyecto/detail/(?P<pk>\S+)/$', administrador.EstadoProyectoDetailView.as_view(), name='Inventario_estadoproyecto_detail'),
    url(r'^Inventario/estadoproyecto/update/(?P<pk>\S+)/$', administrador.EstadoProyectoUpdateView.as_view(), name='Inventario_estadoproyecto_update'),
)

urlpatterns += (
    # urls for ResultadoProyecto
    url(r'^Inventario/resultadoproyecto/$', administrador.ResultadoProyectoListView.as_view(), name='Inventario_resultadoproyecto_list'),
    url(r'^Inventario/resultadoproyecto/create/$', administrador.ResultadoProyectoCreateView.as_view(), name='Inventario_resultadoproyecto_create'),
    url(r'^Inventario/resultadoproyecto/detail/(?P<pk>\S+)/$', administrador.ResultadoProyectoDetailView.as_view(), name='Inventario_resultadoproyecto_detail'),
    url(r'^Inventario/resultadoproyecto/update/(?P<pk>\S+)/$', administrador.ResultadoProyectoUpdateView.as_view(), name='Inventario_resultadoproyecto_update'),
)

urlpatterns += (
    # urls for Recurso_Documento
    url(r'^Inventario/recurso_documento/$', administrador.Recurso_DocumentoListView.as_view(), name='Inventario_recurso_documento_list'),
    url(r'^Inventario/recurso_documento/create/$', administrador.Recurso_DocumentoCreateView.as_view(), name='Inventario_recurso_documento_create'),
    url(r'^Inventario/recurso_documento/(?P<idRecurso>\S+)/$', administrador.Recurso_Documento_Add, name='Inventario_recurso_documento'),
    url(r'^Inventario/recurso_documento/detail/(?P<pk>\S+)/$', administrador.Recurso_DocumentoDetailView.as_view(), name='Inventario_recurso_documento_detail'),
    url(r'^Inventario/recurso_documento/update/(?P<pk>\S+)/$', administrador.Recurso_DocumentoUpdateView.as_view(), name='Inventario_recurso_documento_update'),
)

urlpatterns += (
    # urls for Miembro_Proyecto
    url(r'^Inventario/miembro_proyecto/$', administrador.Miembro_ProyectoListView.as_view(), name='Inventario_miembro_proyecto_list'),
    url(r'^Inventario/miembro_proyecto/create/$', administrador.Miembro_ProyectoCreateView.as_view(), name='Inventario_miembro_proyecto_create'),
    url(r'^Inventario/miembro_proyecto/detail/(?P<idMiembroProyecto>\S+)/$', administrador.Miembro_ProyectoDetail, name='Inventario_miembro_proyecto_detail'),
    url(r'^Inventario/miembro_proyecto/update/(?P<pk>\S+)/$', administrador.Miembro_ProyectoUpdateView.as_view(), name='Inventario_miembro_proyecto_update'),
)

urlpatterns += (
    # urls for Recurso_Proyecto
    url(r'^Inventario/recurso_proyecto/$', administrador.Recurso_ProyectoListView.as_view(), name='Inventario_recurso_proyecto_list'),
    url(r'^Inventario/recurso_proyecto/create/$', administrador.Recurso_ProyectoCreateView.as_view(), name='Inventario_recurso_proyecto_create'),
    url(r'^Inventario/recurso_proyecto/detail/(?P<pk>\S+)/$', administrador.Recurso_ProyectoDetailView.as_view(), name='Inventario_recurso_proyecto_detail'),
    url(r'^Inventario/recurso_proyecto/update/(?P<pk>\S+)/$', administrador.Recurso_ProyectoUpdateView.as_view(), name='Inventario_recurso_proyecto_update'),
)

urlpatterns += (
    # urls for MiembroProyecto_RecursoProyecto
    url(r'^Inventario/miembroproyecto_recursoproyecto/$', administrador.MiembroProyecto_RecursoProyectoListView.as_view(), name='Inventario_miembroproyecto_recursoproyecto_list'),
    url(r'^Inventario/asignarRecursoMiembro/(?P<idProyecto>\S+)/(?P<idMiembroProyecto>\S+)$', administrador.asignarRecursoAMiembro, name='Inventario_asignar_recurso_miembro'),
    url(r'^Inventario/miembroproyecto_recursoproyecto/detail/(?P<pk>\S+)/$', administrador.MiembroProyecto_RecursoProyectoDetailView.as_view(), name='Inventario_miembroproyecto_recursoproyecto_detail'),
    url(r'^Inventario/miembroproyecto_recursoproyecto/update/(?P<pk>\S+)/$', administrador.MiembroProyecto_RecursoProyectoUpdateView.as_view(), name='Inventario_miembroproyecto_recursoproyecto_update'),
    url(r'^Inventario/desasignarRecursoMiembro/$', administrador.desasignarRecursoMiembro, name='Inventario_desasignar_Recurso_Miembro'),
    
    ## eliminar recurso de un proyecto
    url(r'^Inventario/desasignarRecursoProyecto/$', administrador.desasignarRecursoProyecto, name='Inventario_desasignar_Recurso_Proyecto'),
    url(r'^Inventario/desasignarMiembroProyecto/$', administrador.desasignarMiembroProyecto, name='Inventario_desasignar_Miembro_Proyecto'),
)

urlpatterns += (
    url(r'^reportes/$', administrador.reportes, name='reportes'),
    url(r'^reporte_recursos_pdf/$',administrador.ReportResourcePDF.as_view(), name="reporte_recursos_pdf"),
)

urlpatterns += (
    url(r'^solicitudes$', administrador.listar_solicitudes, name='solicitudes'),
    url(r'^aprobar/(?P<idUser>\S+)$', administrador.aprobar_solicitud, name='aprobar'),
    url(r'^rechazar/(?P<idUser>\S+)$', administrador.rechazar_solicitud, name='rechazar'),
    url(r'^inicioadmin/$', administrador.inicio, name='inicioadmin'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)$', administrador.get_user_profile, name='profileAdmin'),
    url(r'^gestionarPrestamos/$', administrador.gestionar_prestamos, name='gestionar_prestamos'),
    url(r'^aceptarSolicitudPrestamo/$', administrador.aceptarSolicitudPrestamo, name='aceptar_solicitud_prestamo'),
    url(r'^rechazarSolicitudPrestamo/$', administrador.rechazarSolicitudPrestamo, name='rechazar_solicitud_prestamo'),
)

# URLs para miembros
urlpatterns += (
    url(r'^perfil/(?P<username>[a-zA-Z0-9]+)$', miembro.get_user_profile, name='profile'), # debe tener su propio index
    url(r'^prestamos/$', miembro.prestamos_listar, name='prestamos_del_miembro'),
    url(r'^editarperfil/(?P<username>[a-zA-Z0-9]+)$', miembro.editar_datos_miembro, name='editar_datos_miembro'),
    url(r'^editarcontrasena/(?P<username>[a-zA-Z0-9]+)$', miembro.editar_miembro_contras, name='editar_miembro_password'),
    url(r'^miembro/solicitarRecurso/$', miembro.solicitarRecurso, name='solicitar_recurso_miembro'),
)

urlpatterns += (
    url(r'^miembro/recurso/detalle/(?P<idRecurso>\S+)$', miembro.detalleRecurso, name='detalle_recurso_miembro'),
    url(r'^miembro/proyecto/detalle/(?P<idProyecto>\S+)$', miembro.detalleProyecto, name='detalle_proyecto_miembro'),
)

# URLs para todos en general (siempre y cuando no hayan iniciado sesión en el sistema
urlpatterns += (
    url(r'^solicitar/$', general.solicitar_cuenta_form, name='solicitar'),
    url(r'^inicio/$', miembro.inicio, name='inicio'),
    url(r'^index/$', general.inicio_funcion, name='index'),
)
