from . import models
from . import serializers
from rest_framework import viewsets, permissions


class recursosViewSet(viewsets.ModelViewSet):
    """ViewSet for the recursos class"""

    queryset = models.recursos.objects.all()
    serializer_class = serializers.recursosSerializer
    permission_classes = [permissions.IsAuthenticated]


class MiembrosViewSet(viewsets.ModelViewSet):
    """ViewSet for the Miembros class"""

    queryset = models.Miembros.objects.all()
    serializer_class = serializers.MiembrosSerializer
    permission_classes = [permissions.IsAuthenticated]


class Historial_RecursosViewSet(viewsets.ModelViewSet):
    """ViewSet for the Historial_Recursos class"""

    queryset = models.Historial_Recursos.objects.all()
    serializer_class = serializers.Historial_RecursosSerializer
    permission_classes = [permissions.IsAuthenticated]


class EstadoRecursoViewSet(viewsets.ModelViewSet):
    """ViewSet for the EstadoRecurso class"""

    queryset = models.EstadoRecurso.objects.all()
    serializer_class = serializers.EstadoRecursoSerializer
    permission_classes = [permissions.IsAuthenticated]


class EntidadViewSet(viewsets.ModelViewSet):
    """ViewSet for the Entidad class"""

    queryset = models.Entidad.objects.all()
    serializer_class = serializers.EntidadSerializer
    permission_classes = [permissions.IsAuthenticated]


class DocumentoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Documento class"""

    queryset = models.Documento.objects.all()
    serializer_class = serializers.DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CargosViewSet(viewsets.ModelViewSet):
    """ViewSet for the Cargos class"""

    queryset = models.Cargos.objects.all()
    serializer_class = serializers.CargosSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProyectosViewSet(viewsets.ModelViewSet):
    """ViewSet for the Proyectos class"""

    queryset = models.Proyectos.objects.all()
    serializer_class = serializers.ProyectosSerializer
    permission_classes = [permissions.IsAuthenticated]


class Historial_ProyectoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Historial_Proyecto class"""

    queryset = models.Historial_Proyecto.objects.all()
    serializer_class = serializers.Historial_ProyectoSerializer
    permission_classes = [permissions.IsAuthenticated]


class EstadoProyectoViewSet(viewsets.ModelViewSet):
    """ViewSet for the EstadoProyecto class"""

    queryset = models.EstadoProyecto.objects.all()
    serializer_class = serializers.EstadoProyectoSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResultadoProyectoViewSet(viewsets.ModelViewSet):
    """ViewSet for the ResultadoProyecto class"""

    queryset = models.ResultadoProyecto.objects.all()
    serializer_class = serializers.ResultadoProyectoSerializer
    permission_classes = [permissions.IsAuthenticated]


class Recurso_DocumentoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Recurso_Documento class"""

    queryset = models.Recurso_Documento.objects.all()
    serializer_class = serializers.Recurso_DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]


class Miembro_ProyectoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Miembro_Proyecto class"""

    queryset = models.Miembro_Proyecto.objects.all()
    serializer_class = serializers.Miembro_ProyectoSerializer
    permission_classes = [permissions.IsAuthenticated]


class Recurso_ProyectoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Recurso_Proyecto class"""

    queryset = models.Recurso_Proyecto.objects.all()
    serializer_class = serializers.Recurso_ProyectoSerializer
    permission_classes = [permissions.IsAuthenticated]


class MiembroProyecto_RecursoProyectoViewSet(viewsets.ModelViewSet):
    """ViewSet for the MiembroProyecto_RecursoProyecto class"""

    queryset = models.MiembroProyecto_RecursoProyecto.objects.all()
    serializer_class = serializers.MiembroProyecto_RecursoProyectoSerializer
    permission_classes = [permissions.IsAuthenticated]


