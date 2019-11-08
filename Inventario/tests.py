# import unittest
# from django.urls import reverse
# from django.test import Client
# from .models import recursos, Miembros, Historial_Recursos, EstadoRecurso, Entidad, Documento, Cargos, Proyectos, Historial_Proyecto, EstadoProyecto, ResultadoProyecto, Recurso_Documento, Miembro_Proyecto, Recurso_Proyecto, MiembroProyecto_RecursoProyecto
# from django.contrib.auth.models import User
# from django.contrib.auth.models import Group
# from django.contrib.contenttypes.models import ContentType
# 
# 
# def create_django_contrib_auth_models_user(**kwargs):
#     defaults = {}
#     defaults["username"] = "username"
#     defaults["email"] = "username@tempurl.com"
#     defaults.update(**kwargs)
#     return User.objects.create(**defaults)
# 
# 
# def create_django_contrib_auth_models_group(**kwargs):
#     defaults = {}
#     defaults["name"] = "group"
#     defaults.update(**kwargs)
#     return Group.objects.create(**defaults)
# 
# 
# def create_django_contrib_contenttypes_models_contenttype(**kwargs):
#     defaults = {}
#     defaults.update(**kwargs)
#     return ContentType.objects.create(**defaults)
# 
# 
# def create_recursos(**kwargs):
#     defaults = {}
#     defaults["cod_patrimonio"] = "cod_patrimonio"
#     defaults["nro_producto"] = "nro_producto"
#     defaults["nro_serie"] = "nro_serie"
#     defaults["nombre"] = "nombre"
#     defaults["fecha_ingreso"] = "fecha_ingreso"
#     defaults["caracteristicas"] = "caracteristicas"
#     defaults["tipo"] = "tipo"
#     defaults.update(**kwargs)
#     return recursos.objects.create(**defaults)
# 
# 
# def create_miembros(**kwargs):
#     defaults = {}
#     defaults["nombre"] = "nombre"
#     defaults["apellido"] = "apellido"
#     defaults["dni"] = "dni"
#     defaults["fecha_ingreso"] = "fecha_ingreso"
#     defaults["foto"] = "foto"
#     defaults["telefono"] = "telefono"
#     defaults["correo"] = "correo"
#     defaults["fecha_nacimiento"] = "fecha_nacimiento"
#     defaults["tipo_miembro"] = "tipo_miembro"
#     defaults.update(**kwargs)
#     return Miembros.objects.create(**defaults)
# 
# 
# def create_historial_recursos(**kwargs):
#     defaults = {}
#     defaults["fecha_historial"] = "fecha_historial"
#     defaults["observaciones"] = "observaciones"
#     defaults.update(**kwargs)
#     if "idRecurso" not in defaults:
#         defaults["idRecurso"] = create_'inventario_recursos'()
#     if "idEstadoRecurso" not in defaults:
#         defaults["idEstadoRecurso"] = create_'inventario_estadorecurso'()
#     return Historial_Recursos.objects.create(**defaults)
# 
# 
# def create_estadorecurso(**kwargs):
#     defaults = {}
#     defaults["descripcion"] = "descripcion"
#     defaults.update(**kwargs)
#     return EstadoRecurso.objects.create(**defaults)
# 
# 
# def create_entidad(**kwargs):
#     defaults = {}
#     defaults["razon_social"] = "razon_social"
#     defaults["ruc"] = "ruc"
#     defaults["telefono"] = "telefono"
#     defaults["correo"] = "correo"
#     defaults["representante_legal"] = "representante_legal"
#     defaults.update(**kwargs)
#     return Entidad.objects.create(**defaults)
# 
# 
# def create_documento(**kwargs):
#     defaults = {}
#     defaults["codigo_documento"] = "codigo_documento"
#     defaults["fecha_emision"] = "fecha_emision"
#     defaults["tipo"] = "tipo"
#     defaults["ruta_pdf"] = "ruta_pdf"
#     defaults["estado"] = "estado"
#     defaults.update(**kwargs)
#     if "entidad" not in defaults:
#         defaults["entidad"] = create_'inventario_entidad'()
#     return Documento.objects.create(**defaults)
# 
# 
# def create_cargos(**kwargs):
#     defaults = {}
#     defaults["descripcion"] = "descripcion"
#     defaults.update(**kwargs)
#     return Cargos.objects.create(**defaults)
# 
# 
# def create_proyectos(**kwargs):
#     defaults = {}
#     defaults["codigo"] = "codigo"
#     defaults["nombre"] = "nombre"
#     defaults["descripcion"] = "descripcion"
#     defaults["fecha_inicio"] = "fecha_inicio"
#     defaults.update(**kwargs)
#     return Proyectos.objects.create(**defaults)
# 
# 
# def create_historial_proyecto(**kwargs):
#     defaults = {}
#     defaults["fecha_historial"] = "fecha_historial"
#     defaults["observaciones"] = "observaciones"
#     defaults.update(**kwargs)
#     if "idProyecto" not in defaults:
#         defaults["idProyecto"] = create_'inventario_proyectos'()
#     if "idEstadoProyecto" not in defaults:
#         defaults["idEstadoProyecto"] = create_'inventario_estadoproyecto'()
#     return Historial_Proyecto.objects.create(**defaults)
# 
# 
# def create_estadoproyecto(**kwargs):
#     defaults = {}
#     defaults["descripcion"] = "descripcion"
#     defaults.update(**kwargs)
#     return EstadoProyecto.objects.create(**defaults)
# 
# 
# def create_resultadoproyecto(**kwargs):
#     defaults = {}
#     defaults["descripcion"] = "descripcion"
#     defaults["fecha_resultado"] = "fecha_resultado"
#     defaults.update(**kwargs)
#     if "idProyecto" not in defaults:
#         defaults["idProyecto"] = create_'inventario_proyectos'()
#     return ResultadoProyecto.objects.create(**defaults)
# 
# 
# def create_recurso_documento(**kwargs):
#     defaults = {}
#     defaults.update(**kwargs)
#     if "idDocumento" not in defaults:
#         defaults["idDocumento"] = create_'inventario_documento'()
#     if "idRecurso" not in defaults:
#         defaults["idRecurso"] = create_'inventario_recursos'()
#     return Recurso_Documento.objects.create(**defaults)
# 
# 
# def create_miembro_proyecto(**kwargs):
#     defaults = {}
#     defaults["descripcion"] = "descripcion"
#     defaults["fecha_miembro_proyecto"] = "fecha_miembro_proyecto"
#     defaults["estado_miembro_proyecto"] = "estado_miembro_proyecto"
#     defaults.update(**kwargs)
#     if "idCargo" not in defaults:
#         defaults["idCargo"] = create_'inventario_cargos'()
#     if "idMiembro" not in defaults:
#         defaults["idMiembro"] = create_'inventario_miembros'()
#     if "idProyecto" not in defaults:
#         defaults["idProyecto"] = create_'inventario_proyectos'()
#     return Miembro_Proyecto.objects.create(**defaults)
# 
# 
# def create_recurso_proyecto(**kwargs):
#     defaults = {}
#     defaults["descripcion"] = "descripcion"
#     defaults["estado"] = "estado"
#     defaults["fecha_recurso_proyecto"] = "fecha_recurso_proyecto"
#     defaults.update(**kwargs)
#     if "idProyecto" not in defaults:
#         defaults["idProyecto"] = create_'inventario_proyectos'()
#     if "idRecurso" not in defaults:
#         defaults["idRecurso"] = create_'inventario_recursos'()
#     return Recurso_Proyecto.objects.create(**defaults)
# 
# 
# def create_miembroproyecto_recursoproyecto(**kwargs):
#     defaults = {}
#     defaults["observacion"] = "observacion"
#     defaults["estado"] = "estado"
#     defaults["fecha"] = "fecha"
#     defaults.update(**kwargs)
#     if "idMiembro_Proyecto" not in defaults:
#         defaults["idMiembro_Proyecto"] = create_'inventario_miembro_proyecto'()
#     if "idRecurso_Proyecto" not in defaults:
#         defaults["idRecurso_Proyecto"] = create_'inventario_recurso_proyecto'()
#     return MiembroProyecto_RecursoProyecto.objects.create(**defaults)
# 
# 
# class recursosViewTest(unittest.TestCase):
#     '''
#     Tests for recursos
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_recursos(self):
#         url = reverse('Inventario_recursos_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_recursos(self):
#         url = reverse('Inventario_recursos_create')
#         data = {
#             "cod_patrimonio": "cod_patrimonio",
#             "nro_producto": "nro_producto",
#             "nro_serie": "nro_serie",
#             "nombre": "nombre",
#             "fecha_ingreso": "fecha_ingreso",
#             "caracteristicas": "caracteristicas",
#             "tipo": "tipo",
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_recursos(self):
#         recursos = create_recursos()
#         url = reverse('Inventario_recursos_detail', args=[recursos.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_recursos(self):
#         recursos = create_recursos()
#         data = {
#             "cod_patrimonio": "cod_patrimonio",
#             "nro_producto": "nro_producto",
#             "nro_serie": "nro_serie",
#             "nombre": "nombre",
#             "fecha_ingreso": "fecha_ingreso",
#             "caracteristicas": "caracteristicas",
#             "tipo": "tipo",
#         }
#         url = reverse('Inventario_recursos_update', args=[recursos.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class MiembrosViewTest(unittest.TestCase):
#     '''
#     Tests for Miembros
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_miembros(self):
#         url = reverse('Inventario_miembros_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_miembros(self):
#         url = reverse('Inventario_miembros_create')
#         data = {
#             "nombre": "nombre",
#             "apellido": "apellido",
#             "dni": "dni",
#             "fecha_ingreso": "fecha_ingreso",
#             "foto": "foto",
#             "telefono": "telefono",
#             "correo": "correo",
#             "fecha_nacimiento": "fecha_nacimiento",
#             "tipo_miembro": "tipo_miembro",
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_miembros(self):
#         miembros = create_miembros()
#         url = reverse('Inventario_miembros_detail', args=[miembros.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_miembros(self):
#         miembros = create_miembros()
#         data = {
#             "nombre": "nombre",
#             "apellido": "apellido",
#             "dni": "dni",
#             "fecha_ingreso": "fecha_ingreso",
#             "foto": "foto",
#             "telefono": "telefono",
#             "correo": "correo",
#             "fecha_nacimiento": "fecha_nacimiento",
#             "tipo_miembro": "tipo_miembro",
#         }
#         url = reverse('Inventario_miembros_update', args=[miembros.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class Historial_RecursosViewTest(unittest.TestCase):
#     '''
#     Tests for Historial_Recursos
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_historial_recursos(self):
#         url = reverse('Inventario_historial_recursos_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_historial_recursos(self):
#         url = reverse('Inventario_historial_recursos_create')
#         data = {
#             "fecha_historial": "fecha_historial",
#             "observaciones": "observaciones",
#             "idRecurso": create_'inventario_recursos'().pk,
#             "idEstadoRecurso": create_'inventario_estadorecurso'().pk,
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_historial_recursos(self):
#         historial_recursos = create_historial_recursos()
#         url = reverse('Inventario_historial_recursos_detail', args=[historial_recursos.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_historial_recursos(self):
#         historial_recursos = create_historial_recursos()
#         data = {
#             "fecha_historial": "fecha_historial",
#             "observaciones": "observaciones",
#             "idRecurso": create_'inventario_recursos'().pk,
#             "idEstadoRecurso": create_'inventario_estadorecurso'().pk,
#         }
#         url = reverse('Inventario_historial_recursos_update', args=[historial_recursos.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class EstadoRecursoViewTest(unittest.TestCase):
#     '''
#     Tests for EstadoRecurso
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_estadorecurso(self):
#         url = reverse('Inventario_estadorecurso_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_estadorecurso(self):
#         url = reverse('Inventario_estadorecurso_create')
#         data = {
#             "descripcion": "descripcion",
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_estadorecurso(self):
#         estadorecurso = create_estadorecurso()
#         url = reverse('Inventario_estadorecurso_detail', args=[estadorecurso.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_estadorecurso(self):
#         estadorecurso = create_estadorecurso()
#         data = {
#             "descripcion": "descripcion",
#         }
#         url = reverse('Inventario_estadorecurso_update', args=[estadorecurso.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class EntidadViewTest(unittest.TestCase):
#     '''
#     Tests for Entidad
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_entidad(self):
#         url = reverse('Inventario_entidad_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_entidad(self):
#         url = reverse('Inventario_entidad_create')
#         data = {
#             "razon_social": "razon_social",
#             "ruc": "ruc",
#             "telefono": "telefono",
#             "correo": "correo",
#             "representante_legal": "representante_legal",
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_entidad(self):
#         entidad = create_entidad()
#         url = reverse('Inventario_entidad_detail', args=[entidad.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_entidad(self):
#         entidad = create_entidad()
#         data = {
#             "razon_social": "razon_social",
#             "ruc": "ruc",
#             "telefono": "telefono",
#             "correo": "correo",
#             "representante_legal": "representante_legal",
#         }
#         url = reverse('Inventario_entidad_update', args=[entidad.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class DocumentoViewTest(unittest.TestCase):
#     '''
#     Tests for Documento
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_documento(self):
#         url = reverse('Inventario_documento_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_documento(self):
#         url = reverse('Inventario_documento_create')
#         data = {
#             "codigo_documento": "codigo_documento",
#             "fecha_emision": "fecha_emision",
#             "tipo": "tipo",
#             "ruta_pdf": "ruta_pdf",
#             "estado": "estado",
#             "entidad": create_'inventario_entidad'().pk,
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_documento(self):
#         documento = create_documento()
#         url = reverse('Inventario_documento_detail', args=[documento.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_documento(self):
#         documento = create_documento()
#         data = {
#             "codigo_documento": "codigo_documento",
#             "fecha_emision": "fecha_emision",
#             "tipo": "tipo",
#             "ruta_pdf": "ruta_pdf",
#             "estado": "estado",
#             "entidad": create_'inventario_entidad'().pk,
#         }
#         url = reverse('Inventario_documento_update', args=[documento.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class CargosViewTest(unittest.TestCase):
#     '''
#     Tests for Cargos
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_cargos(self):
#         url = reverse('Inventario_cargos_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_cargos(self):
#         url = reverse('Inventario_cargos_create')
#         data = {
#             "descripcion": "descripcion",
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_cargos(self):
#         cargos = create_cargos()
#         url = reverse('Inventario_cargos_detail', args=[cargos.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_cargos(self):
#         cargos = create_cargos()
#         data = {
#             "descripcion": "descripcion",
#         }
#         url = reverse('Inventario_cargos_update', args=[cargos.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class ProyectosViewTest(unittest.TestCase):
#     '''
#     Tests for Proyectos
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_proyectos(self):
#         url = reverse('Inventario_proyectos_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_proyectos(self):
#         url = reverse('Inventario_proyectos_create')
#         data = {
#             "codigo": "codigo",
#             "nombre": "nombre",
#             "descripcion": "descripcion",
#             "fecha_inicio": "fecha_inicio",
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_proyectos(self):
#         proyectos = create_proyectos()
#         url = reverse('Inventario_proyectos_detail', args=[proyectos.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_proyectos(self):
#         proyectos = create_proyectos()
#         data = {
#             "codigo": "codigo",
#             "nombre": "nombre",
#             "descripcion": "descripcion",
#             "fecha_inicio": "fecha_inicio",
#         }
#         url = reverse('Inventario_proyectos_update', args=[proyectos.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class Historial_ProyectoViewTest(unittest.TestCase):
#     '''
#     Tests for Historial_Proyecto
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_historial_proyecto(self):
#         url = reverse('Inventario_historial_proyecto_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_historial_proyecto(self):
#         url = reverse('Inventario_historial_proyecto_create')
#         data = {
#             "fecha_historial": "fecha_historial",
#             "observaciones": "observaciones",
#             "idProyecto": create_'inventario_proyectos'().pk,
#             "idEstadoProyecto": create_'inventario_estadoproyecto'().pk,
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_historial_proyecto(self):
#         historial_proyecto = create_historial_proyecto()
#         url = reverse('Inventario_historial_proyecto_detail', args=[historial_proyecto.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_historial_proyecto(self):
#         historial_proyecto = create_historial_proyecto()
#         data = {
#             "fecha_historial": "fecha_historial",
#             "observaciones": "observaciones",
#             "idProyecto": create_'inventario_proyectos'().pk,
#             "idEstadoProyecto": create_'inventario_estadoproyecto'().pk,
#         }
#         url = reverse('Inventario_historial_proyecto_update', args=[historial_proyecto.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class EstadoProyectoViewTest(unittest.TestCase):
#     '''
#     Tests for EstadoProyecto
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_estadoproyecto(self):
#         url = reverse('Inventario_estadoproyecto_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_estadoproyecto(self):
#         url = reverse('Inventario_estadoproyecto_create')
#         data = {
#             "descripcion": "descripcion",
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_estadoproyecto(self):
#         estadoproyecto = create_estadoproyecto()
#         url = reverse('Inventario_estadoproyecto_detail', args=[estadoproyecto.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_estadoproyecto(self):
#         estadoproyecto = create_estadoproyecto()
#         data = {
#             "descripcion": "descripcion",
#         }
#         url = reverse('Inventario_estadoproyecto_update', args=[estadoproyecto.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class ResultadoProyectoViewTest(unittest.TestCase):
#     '''
#     Tests for ResultadoProyecto
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_resultadoproyecto(self):
#         url = reverse('Inventario_resultadoproyecto_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_resultadoproyecto(self):
#         url = reverse('Inventario_resultadoproyecto_create')
#         data = {
#             "descripcion": "descripcion",
#             "fecha_resultado": "fecha_resultado",
#             "idProyecto": create_'inventario_proyectos'().pk,
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_resultadoproyecto(self):
#         resultadoproyecto = create_resultadoproyecto()
#         url = reverse('Inventario_resultadoproyecto_detail', args=[resultadoproyecto.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_resultadoproyecto(self):
#         resultadoproyecto = create_resultadoproyecto()
#         data = {
#             "descripcion": "descripcion",
#             "fecha_resultado": "fecha_resultado",
#             "idProyecto": create_'inventario_proyectos'().pk,
#         }
#         url = reverse('Inventario_resultadoproyecto_update', args=[resultadoproyecto.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class Recurso_DocumentoViewTest(unittest.TestCase):
#     '''
#     Tests for Recurso_Documento
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_recurso_documento(self):
#         url = reverse('Inventario_recurso_documento_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_recurso_documento(self):
#         url = reverse('Inventario_recurso_documento_create')
#         data = {
#             "idDocumento": create_'inventario_documento'().pk,
#             "idRecurso": create_'inventario_recursos'().pk,
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_recurso_documento(self):
#         recurso_documento = create_recurso_documento()
#         url = reverse('Inventario_recurso_documento_detail', args=[recurso_documento.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_recurso_documento(self):
#         recurso_documento = create_recurso_documento()
#         data = {
#             "idDocumento": create_'inventario_documento'().pk,
#             "idRecurso": create_'inventario_recursos'().pk,
#         }
#         url = reverse('Inventario_recurso_documento_update', args=[recurso_documento.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class Miembro_ProyectoViewTest(unittest.TestCase):
#     '''
#     Tests for Miembro_Proyecto
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_miembro_proyecto(self):
#         url = reverse('Inventario_miembro_proyecto_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_miembro_proyecto(self):
#         url = reverse('Inventario_miembro_proyecto_create')
#         data = {
#             "descripcion": "descripcion",
#             "fecha_miembro_proyecto": "fecha_miembro_proyecto",
#             "estado_miembro_proyecto": "estado_miembro_proyecto",
#             "idCargo": create_'inventario_cargos'().pk,
#             "idMiembro": create_'inventario_miembros'().pk,
#             "idProyecto": create_'inventario_proyectos'().pk,
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_miembro_proyecto(self):
#         miembro_proyecto = create_miembro_proyecto()
#         url = reverse('Inventario_miembro_proyecto_detail', args=[miembro_proyecto.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_miembro_proyecto(self):
#         miembro_proyecto = create_miembro_proyecto()
#         data = {
#             "descripcion": "descripcion",
#             "fecha_miembro_proyecto": "fecha_miembro_proyecto",
#             "estado_miembro_proyecto": "estado_miembro_proyecto",
#             "idCargo": create_'inventario_cargos'().pk,
#             "idMiembro": create_'inventario_miembros'().pk,
#             "idProyecto": create_'inventario_proyectos'().pk,
#         }
#         url = reverse('Inventario_miembro_proyecto_update', args=[miembro_proyecto.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class Recurso_ProyectoViewTest(unittest.TestCase):
#     '''
#     Tests for Recurso_Proyecto
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_recurso_proyecto(self):
#         url = reverse('Inventario_recurso_proyecto_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_recurso_proyecto(self):
#         url = reverse('Inventario_recurso_proyecto_create')
#         data = {
#             "descripcion": "descripcion",
#             "estado": "estado",
#             "fecha_recurso_proyecto": "fecha_recurso_proyecto",
#             "idProyecto": create_'inventario_proyectos'().pk,
#             "idRecurso": create_'inventario_recursos'().pk,
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_recurso_proyecto(self):
#         recurso_proyecto = create_recurso_proyecto()
#         url = reverse('Inventario_recurso_proyecto_detail', args=[recurso_proyecto.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_recurso_proyecto(self):
#         recurso_proyecto = create_recurso_proyecto()
#         data = {
#             "descripcion": "descripcion",
#             "estado": "estado",
#             "fecha_recurso_proyecto": "fecha_recurso_proyecto",
#             "idProyecto": create_'inventario_proyectos'().pk,
#             "idRecurso": create_'inventario_recursos'().pk,
#         }
#         url = reverse('Inventario_recurso_proyecto_update', args=[recurso_proyecto.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)
# 
# 
# class MiembroProyecto_RecursoProyectoViewTest(unittest.TestCase):
#     '''
#     Tests for MiembroProyecto_RecursoProyecto
#     '''
#     def setUp(self):
#         self.client = Client()
# 
#     def test_list_miembroproyecto_recursoproyecto(self):
#         url = reverse('Inventario_miembroproyecto_recursoproyecto_list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_create_miembroproyecto_recursoproyecto(self):
#         url = reverse('Inventario_miembroproyecto_recursoproyecto_create')
#         data = {
#             "observacion": "observacion",
#             "estado": "estado",
#             "fecha": "fecha",
#             "idMiembro_Proyecto": create_'inventario_miembro_proyecto'().pk,
#             "idRecurso_Proyecto": create_'inventario_recurso_proyecto'().pk,
#         }
#         response = self.client.post(url, data=data)
#         self.assertEqual(response.status_code, 302)
# 
#     def test_detail_miembroproyecto_recursoproyecto(self):
#         miembroproyecto_recursoproyecto = create_miembroproyecto_recursoproyecto()
#         url = reverse('Inventario_miembroproyecto_recursoproyecto_detail', args=[miembroproyecto_recursoproyecto.pk,])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
# 
#     def test_update_miembroproyecto_recursoproyecto(self):
#         miembroproyecto_recursoproyecto = create_miembroproyecto_recursoproyecto()
#         data = {
#             "observacion": "observacion",
#             "estado": "estado",
#             "fecha": "fecha",
#             "idMiembro_Proyecto": create_'inventario_miembro_proyecto'().pk,
#             "idRecurso_Proyecto": create_'inventario_recurso_proyecto'().pk,
#         }
#         url = reverse('Inventario_miembroproyecto_recursoproyecto_update', args=[miembroproyecto_recursoproyecto.pk,])
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 302)


