from . import models

from rest_framework import serializers


class recursosSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.recursos
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'cod_patrimonio', 
            'nro_producto', 
            'nro_serie', 
            'nombre',
            'foto',
            'fecha_ingreso', 
            'caracteristicas', 
            'tipo', 
        )


class MiembrosSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Miembros
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'nombre', 
            'apellido', 
            'dni', 
            'password',
            'fecha_ingreso', 
            'foto', 
            'telefono', 
            'correo', 
            'fecha_nacimiento', 
            'tipo_miembro', 
        )


class Historial_RecursosSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Historial_Recursos
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'fecha_historial', 
            'observaciones', 
        )


class EstadoRecursoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EstadoRecurso
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'descripcion', 
        )


class EntidadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Entidad
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'razon_social', 
            'ruc', 
            'telefono', 
            'correo', 
            'representante_legal', 
        )


class DocumentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Documento
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'codigo_documento', 
            'fecha_emision', 
            'tipo', 
            'ruta_pdf', 
            'estado', 
        )


class CargosSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cargos
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'descripcion', 
        )


class ProyectosSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Proyectos
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'codigo', 
            'nombre', 
            'descripcion', 
            'fecha_inicio', 
        )


class Historial_ProyectoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Historial_Proyecto
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'fecha_historial', 
            'observaciones', 
        )


class EstadoProyectoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EstadoProyecto
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'descripcion', 
        )


class ResultadoProyectoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ResultadoProyecto
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'descripcion', 
            'fecha_resultado', 
        )


class Recurso_DocumentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recurso_Documento
        fields = (
            'pk', 
            'created', 
            'last_updated', 
        )


class Miembro_ProyectoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Miembro_Proyecto
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'descripcion', 
            'fecha_miembro_proyecto', 
            'estado_miembro_proyecto', 
        )


class Recurso_ProyectoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recurso_Proyecto
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'descripcion', 
            'estado', 
            'fecha_recurso_proyecto', 
        )


class MiembroProyecto_RecursoProyectoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MiembroProyecto_RecursoProyecto
        fields = (
            'pk', 
            'created', 
            'last_updated', 
            'observacion', 
            'estado', 
            'fecha', 
        )


