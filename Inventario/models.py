from django.urls import reverse
from django.db.models import *

from django.db import models as models
from django.contrib.auth.models import User
import datetime
from django.template.defaultfilters import default

class recursos(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    cod_patrimonio = CharField(max_length=50)
    nro_producto = CharField(max_length=50)
    nro_serie = CharField(max_length=50)
    nombre = CharField(max_length=100)
    foto = ImageField(upload_to='images/recursos/', default = 'images/recursos/None/no-img.jpg')
    fecha_ingreso = DateField(max_length=100)
    caracteristicas = TextField(max_length=100)
    TANGIBLES = 'Tangibles'
    INTANGIBLES = 'Intangibles'
    tipo_lista = (
        (TANGIBLES, 'Tangibles'),
        (INTANGIBLES, 'Intangibles'),
    )
    tipo = CharField(
        max_length= 50,
        choices = tipo_lista,
        default = TANGIBLES,
    )    
    ACTIVO =  'ACTIVO'
    INACTIVO = 'INACTIVO'
    estado_lista = (
        (ACTIVO, 'ACTIVO'),
        (INACTIVO, 'INACTIVO'),
    )
    estado = CharField(
        max_length= 10,
        choices = estado_lista,
        default = ACTIVO,
    )
    
    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        
        return reverse('Inventario_recursos_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_recursos_update', args=(self.pk,))

    def __str__(self):
        return '{}'.format(self.nombre)
    
class Miembros(models.Model):

    # Fields
    user = models.OneToOneField(User, related_name='Miembros', on_delete=models.CASCADE)
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    nombre = CharField(max_length=80)
    apellido = CharField(max_length=80)
    dni = CharField(max_length=30)
    fecha_ingreso = DateField(default = datetime.date.today)
    foto = ImageField(upload_to='images/miembros/', default = 'images/miembros/None/no-img.jpg')
    telefono = CharField(max_length=50)
    correo = CharField(max_length=60)
    fecha_nacimiento = DateField(default = datetime.date.today)
    aleatorio = CharField(max_length=25, default="QAWSEDRFTYUHI")
    EstudiantePregrado = 'Estudiante de Pregrado'
    EstudiantePostgrado= 'Estudiante de Postgrado'
    Magister = 'Magister'
    Doctor = 'Doctor'
    grados_lista = (
        (EstudiantePregrado, 'Estudiante de Pregrado'),
        (EstudiantePostgrado, 'Estudiante de Postgrado'),
        (Magister, 'Magister'),
        (Doctor, 'Doctor'),
    )
    grado_academico = CharField(
        max_length= 50,
        choices = grados_lista,
        default = EstudiantePregrado,
    )

    ACTIVO =  'ACTIVO'
    INACTIVO = 'INACTIVO'
    PENDIENTE = 'PENDIENTE'
    estado_miembro_lista = (
        (ACTIVO, 'ACTIVO'),
        (INACTIVO, 'INACTIVO'),
        (PENDIENTE, 'PENDIENTE'),
    )
    estado_miembro = CharField(
        max_length= 10,
        choices = estado_miembro_lista,
        default = PENDIENTE,
    )
    
    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_miembros_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_miembros_update', args=(self.pk,))
     
    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)
    
class Historial_Recursos(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    fecha_historial = DateField()
    observaciones = TextField()

    # Relationship Fields
    idRecurso = ForeignKey('Inventario.recursos', on_delete=models.CASCADE)
    idEstadoRecurso = ForeignKey('Inventario.EstadoRecurso', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_historial_recursos_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_historial_recursos_update', args=(self.pk,))

    
class EstadoRecurso(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    descripcion = CharField(max_length=60)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_estadorecurso_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_estadorecurso_update', args=(self.pk,))
    
    def __str__(self):
        return '{} '.format(self.descripcion)

class Entidad(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    razon_social = CharField(max_length=100)
    ruc = CharField(max_length=30)
    telefono = CharField(max_length=30)
    correo = CharField(max_length=60)
    representante_legal = CharField(max_length=100)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_entidad_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_entidad_update', args=(self.pk,))
    
    def __str__(self):
        return '{}'.format(self.razon_social)

class Documento(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    codigo_documento = CharField(max_length=300)
    fecha_emision = DateField()
    ruta_pdf = FileField(upload_to='docs/documentos/', default = 'docs/documentos/None/no-img.jpg')
    estado = CharField(max_length=30)
    FACTURA_BOLETA = 'FACTURA_BOLETA'
    GUIA_REMISION= 'GUIA DE REMISION'
    ORDEN_COMPRA= 'ORDEN DE COMPRA'
    ACTA_COMFORMIDAD= 'ACTA DE CONFORMIDAD'
    COMPROBANTE_SALIDA= 'COMPROBANTE DE SALIDA' 
    GARANTIAS= 'GARANTIAS'
    TRASLADOS= 'TRASLADOS'
    OTROS= 'OTROS'  
    tipo_lista = (
        (FACTURA_BOLETA,'FACTURA BOLETA'),
        (GUIA_REMISION,'GUIA DE REMISION'),
        (ORDEN_COMPRA,'ORDEN DE COMPRA'),
        (ACTA_COMFORMIDAD,'ACTA DE CONFORMIDAD'),
        (COMPROBANTE_SALIDA,'COMPROBANTE DE SALIDA'),
        (GARANTIAS,'GARANTIAS'),
        (TRASLADOS,'TRASLADOS'),
        (OTROS,'OTROS'),
    )
    tipo = CharField(
        max_length= 50,
        choices = tipo_lista,
        default = FACTURA_BOLETA
    )

    # Relationship Fields
    entidad = ForeignKey('Inventario.Entidad', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_documento_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('Inventario_documento_update', args=(self.pk,))
    
    def __str__(self):
        return '{} {}'.format(self.tipo, self.codigo_documento)

class Cargos(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    descripcion = CharField(max_length=60)


    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_cargos_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_cargos_update', args=(self.pk,))
    
    def __str__(self):
        return '{}'.format(self.descripcion)

class Proyectos(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    codigo = CharField(max_length=30)
    nombre = CharField(max_length=500)
    descripcion = TextField()
    fecha_inicio = DateField(max_length=100)
    foto = ImageField(upload_to='images/proyectos/', default = 'images/proyectos/None/no-img.jpg')
    estado = CharField(max_length=50, default='ACTIVO')

    class Meta:
        ordering = ('nombre',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_proyectos_detalle', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_proyectos_update', args=(self.pk,))

    def __str__(self):
        return '{}'.format(self.nombre)
    
    
class Historial_Proyecto(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    fecha_historial = DateField()
    observaciones = TextField()

    # Relationship Fields
    idProyecto = ForeignKey('Inventario.Proyectos', on_delete=models.CASCADE)
    idEstadoProyecto = ForeignKey('Inventario.EstadoProyecto', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_historial_proyecto_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_historial_proyecto_update', args=(self.pk,))


class EstadoProyecto(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    descripcion = CharField(max_length=30)


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_estadoproyecto_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_estadoproyecto_update', args=(self.pk,))
    
    def __str__(self):
        return '{}'.format(self.descripcion)

class ResultadoProyecto(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    descripcion = TextField()
    fecha_resultado = DateField()

    # Relationship Fields
    idProyecto = ForeignKey('Inventario.Proyectos', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_resultadoproyecto_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_resultadoproyecto_update', args=(self.pk,))

    
    def __str__(self):
        return '{}'.format(self.descripcion)

class Recurso_Documento(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)

    # Relationship Fields
    idDocumento = ForeignKey('Inventario.Documento', on_delete=models.CASCADE)
    idRecurso = ForeignKey('Inventario.recursos',  on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_recurso_documento_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_recurso_documento_update', args=(self.pk,))

    

class Miembro_Proyecto(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    descripcion = TextField()
    fecha_miembro_proyecto = DateField()
    ACTIVO = 'ACTIVO'
    INACTIVO = 'INACTIVO'
    estado_lista = (
        (ACTIVO, 'ACTIVO'),
        (INACTIVO, 'INACTIVO'),
    )
    estado_miembro_proyecto = CharField(
        max_length= 50,
        choices = estado_lista,
        default = ACTIVO
    )

    # Relationship Fields
    idCargo = ForeignKey('Inventario.Cargos', on_delete=models.CASCADE)
    idMiembro = ForeignKey('Inventario.Miembros', on_delete=models.CASCADE)
    idProyecto = ForeignKey('Inventario.Proyectos', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-idProyecto',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_miembro_proyecto_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_miembro_proyecto_update', args=(self.pk,))
    
    def __str__(self):
        return '{} - {}'.format(self.idProyecto, self.idMiembro)
    
class Recurso_Proyecto(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    descripcion = CharField(max_length=300)
    ACTIVO = 'ACTIVO'
    INACTIVO = 'INACTIVO'
    estado_lista = (
        (ACTIVO, 'ACTIVO'),
        (INACTIVO, 'INACTIVO'),
    )
    estado = CharField(
        max_length= 50,
        choices = estado_lista,
        default = ACTIVO
    )
    fecha_recurso_proyecto = DateField(default = datetime.date.today)

    # Relationship Fields
    idProyecto = ForeignKey('Inventario.Proyectos', on_delete=models.CASCADE)
    idRecurso = ForeignKey('Inventario.recursos', related_name='rn_recurso', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-idProyecto',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_recurso_proyecto_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_recurso_proyecto_update', args=(self.pk,))
    
    def __str__(self):
        return '{} - {} - {}'.format(self.idProyecto, self.idRecurso, self.idRecurso.nro_serie)


class MiembroProyecto_RecursoProyecto(models.Model):

    # Fields
    created = DateTimeField(auto_now_add=True, editable=False)
    last_updated = DateTimeField(auto_now=True, editable=False)
    observacion = TextField()
    SOLICITADO = 'SOLICITADO'
    DENEGADO = 'DENEGADO'
    PRESTADO = 'PRESTADO'
    DEVUELTO = 'DEVUELTO'
    OBSERVADO = 'OBSERVADO'
    estado_lista = (
        (SOLICITADO, 'SOLICITADO'),
        (DENEGADO, 'DENEGADO'),
        (PRESTADO, 'PRESTADO'),
        (DEVUELTO, 'DEVUELTO'),
        (OBSERVADO, 'OBSERVADO'),
    )
    estado = CharField(
        max_length= 50,
        choices = estado_lista,
        default = SOLICITADO
    )
    fecha = DateField(default= datetime.date.today)

    # Relationship Fields
    idMiembro_Proyecto = ForeignKey('Inventario.Miembro_Proyecto', on_delete=models.CASCADE)
    idRecurso_Proyecto = ForeignKey('Inventario.Recurso_Proyecto', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('Inventario_miembroproyecto_recursoproyecto_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('Inventario_miembroproyecto_recursoproyecto_update', args=(self.pk,))
    
    def __str__(self):
        return '{} {}'.format(self.idMiembro_Proyecto, self.idRecurso_Proyecto)
