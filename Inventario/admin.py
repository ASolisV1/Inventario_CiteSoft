from django.contrib import admin
from django import forms
from .models import recursos, Miembros, Historial_Recursos, EstadoRecurso, Entidad, Documento, Cargos, Proyectos, Historial_Proyecto, EstadoProyecto, ResultadoProyecto, Recurso_Documento, Miembro_Proyecto, Recurso_Proyecto, MiembroProyecto_RecursoProyecto
from django.utils.html import format_html

class recursosAdminForm(forms.ModelForm):

    class Meta:
        model = recursos
        fields = '__all__'


class recursosAdmin(admin.ModelAdmin):
    form = recursosAdminForm
    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.foto.url))
    image_tag.short_description = 'Imagen'
    list_display = ['cod_patrimonio', 'nro_producto', 'nro_serie', 'nombre', 'image_tag', 'fecha_ingreso', 'caracteristicas', 'tipo', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated', 'image_tag',]

admin.site.register(recursos, recursosAdmin)


class MiembrosAdminForm(forms.ModelForm):

    class Meta:
        model = Miembros
        fields = '__all__'


class MiembrosAdmin(admin.ModelAdmin):
    form = MiembrosAdminForm
    def image_miembro(self, obj):
        return format_html('<img src="{}" />'.format(obj.foto.url))
    image_miembro.short_description = 'Imagen'
    list_display = ['nombre', 'apellido', 'image_miembro', 'dni', 'fecha_ingreso', 'telefono', 'correo', 'fecha_nacimiento', 'grado_academico', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated', 'image_miembro']

admin.site.register(Miembros, MiembrosAdmin)

class Historial_RecursosAdminForm(forms.ModelForm):

    class Meta:
        model = Historial_Recursos
        fields = '__all__'


class Historial_RecursosAdmin(admin.ModelAdmin):
    form = Historial_RecursosAdminForm
    list_display = ['fecha_historial', 'observaciones', 'created']
    readonly_fields = ['created', 'last_updated']

admin.site.register(Historial_Recursos, Historial_RecursosAdmin)


class EstadoRecursoAdminForm(forms.ModelForm):

    class Meta:
        model = EstadoRecurso
        fields = '__all__'


class EstadoRecursoAdmin(admin.ModelAdmin):
    form = EstadoRecursoAdminForm
    list_display = ['created', 'last_updated', 'descripcion']
    readonly_fields = ['created', 'last_updated']

admin.site.register(EstadoRecurso, EstadoRecursoAdmin)


class EntidadAdminForm(forms.ModelForm):

    class Meta:
        model = Entidad
        fields = '__all__'


class EntidadAdmin(admin.ModelAdmin):
    form = EntidadAdminForm
    list_display = ['razon_social', 'ruc', 'telefono', 'correo', 'representante_legal', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

admin.site.register(Entidad, EntidadAdmin)


class DocumentoAdminForm(forms.ModelForm):

    class Meta:
        model = Documento
        fields = '__all__'


class DocumentoAdmin(admin.ModelAdmin):
    form = DocumentoAdminForm
    list_display = ['codigo_documento', 'fecha_emision', 'tipo', 'ruta_pdf', 'estado', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

admin.site.register(Documento, DocumentoAdmin)


class CargosAdminForm(forms.ModelForm):

    class Meta:
        model = Cargos
        fields = '__all__'


class CargosAdmin(admin.ModelAdmin):
    form = CargosAdminForm
    list_display = ['descripcion', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

def changelist_view(self, request, extra_context = None):
    extra_context = {'title': 'Oye no lo sè.'}
    return super(CargosAdmin, self).changelist_view(request, extra_context=extra_context)
    
admin.site.register(Cargos, CargosAdmin)


class ProyectosAdminForm(forms.ModelForm):

    class Meta:
        model = Proyectos
        fields = '__all__'


class ProyectosAdmin(admin.ModelAdmin):
    form = ProyectosAdminForm
    list_display = ['codigo', 'nombre', 'descripcion', 'fecha_inicio', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

admin.site.register(Proyectos, ProyectosAdmin)


class Historial_ProyectoAdminForm(forms.ModelForm):

    class Meta:
        model = Historial_Proyecto
        fields = '__all__'


class Historial_ProyectoAdmin(admin.ModelAdmin):
    form = Historial_ProyectoAdminForm
    list_display = ['fecha_historial', 'observaciones', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

admin.site.register(Historial_Proyecto, Historial_ProyectoAdmin)


class EstadoProyectoAdminForm(forms.ModelForm):

    class Meta:
        model = EstadoProyecto
        fields = '__all__'


class EstadoProyectoAdmin(admin.ModelAdmin):
    form = EstadoProyectoAdminForm
    list_display = ['descripcion', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

admin.site.register(EstadoProyecto, EstadoProyectoAdmin)


class ResultadoProyectoAdminForm(forms.ModelForm):

    class Meta:
        model = ResultadoProyecto
        fields = '__all__'


class ResultadoProyectoAdmin(admin.ModelAdmin):
    form = ResultadoProyectoAdminForm
    list_display = ['descripcion', 'fecha_resultado', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

admin.site.register(ResultadoProyecto, ResultadoProyectoAdmin)


class Recurso_DocumentoAdminForm(forms.ModelForm):

    class Meta:
        model = Recurso_Documento
        fields = '__all__'


class Recurso_DocumentoAdmin(admin.ModelAdmin):
    form = Recurso_DocumentoAdminForm
    list_display = ['created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

admin.site.register(Recurso_Documento, Recurso_DocumentoAdmin)


class Miembro_ProyectoAdminForm(forms.ModelForm):

    class Meta:
        model = Miembro_Proyecto
        fields = '__all__'


class Miembro_ProyectoAdmin(admin.ModelAdmin):
    form = Miembro_ProyectoAdminForm
    list_display = ['descripcion', 'fecha_miembro_proyecto', 'estado_miembro_proyecto', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

admin.site.register(Miembro_Proyecto, Miembro_ProyectoAdmin)


class Recurso_ProyectoAdminForm(forms.ModelForm):

    class Meta:
        model = Recurso_Proyecto
        fields = '__all__'


class Recurso_ProyectoAdmin(admin.ModelAdmin):
    form = Recurso_ProyectoAdminForm
    list_display = ['descripcion', 'estado', 'fecha_recurso_proyecto', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

admin.site.register(Recurso_Proyecto, Recurso_ProyectoAdmin)


class MiembroProyecto_RecursoProyectoAdminForm(forms.ModelForm):

    class Meta:
        model = MiembroProyecto_RecursoProyecto
        fields = '__all__'


class MiembroProyecto_RecursoProyectoAdmin(admin.ModelAdmin):
    form = MiembroProyecto_RecursoProyectoAdminForm
    list_display = ['observacion', 'estado', 'fecha', 'created', 'last_updated']
    readonly_fields = ['created', 'last_updated']

admin.site.register(MiembroProyecto_RecursoProyecto, MiembroProyecto_RecursoProyectoAdmin)


