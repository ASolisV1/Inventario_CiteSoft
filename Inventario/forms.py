from django import forms
from .models import recursos, Miembros, Historial_Recursos, EstadoRecurso, Entidad, Documento, Cargos, Proyectos, Historial_Proyecto, EstadoProyecto, ResultadoProyecto, Recurso_Documento, Miembro_Proyecto, Recurso_Proyecto, MiembroProyecto_RecursoProyecto
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput

class buscarRecursosForm(forms.ModelForm):
    class Meta:
        model = recursos
        fields = ['nombre']

class buscarMiembrosForm(forms.ModelForm):
    class Meta:
        model = Miembros
        fields = ['nombre']


class recursosForm(forms.ModelForm):
    class Meta:
        model = recursos
        fields = ['nombre', 'tipo']
        widgets = {'fecha_ingreso' : forms.DateInput(format=('%d-%m-%Y')),
                    'tipo': forms.Select(attrs={'class':'form-control'})
        }
        
class recursoEditForm(forms.ModelForm):
    class Meta:
        model = recursos
        fields = ['nombre', 'foto', 'fecha_ingreso', 'caracteristicas', 'tipo']
        widgets = { 'fecha_ingreso': DatePickerInput(format='%d/%m/%Y', attrs={'type': 'datepicker', 'name': 'fecha', 'class':'form-control datepicker','id':'fecha'}),
        }
        
class SolicitarRegistroForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {'first_name': forms.TextInput(attrs={'placeholder': 'Nombres', 'required':''}), 
        'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos', 'required':''}),
        'username' : forms.TextInput(attrs={'placeholder': 'DNI'}), 
        'email' : forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'required':''})}

class MiembrosForm(forms.ModelForm):
    class Meta:
        model = Miembros
        fields = ['nombre','apellido', 'dni', 'foto', 'telefono', 'correo', 'fecha_ingreso', 'fecha_nacimiento', 'grado_academico']
        widgets = {'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombres', 'required':''}), 
        'apellido': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apellidos', 'required':''}),
        'dni' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'DNI', 'readonly':''}), 
        'telefono' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Celular', 'required':''}),
        'correo' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Correo electrónico', 'required':'', 'readonly':''}),
        'fecha_ingreso' : forms.TextInput(attrs={'class':'form-control', 'readonly':''}),
        'grado_academico' : forms.Select(attrs={'class':'form-control'}),
        }
        
class MiembrosEditForm(forms.ModelForm):
    class Meta:
        model = Miembros
        fields = ['nombre','apellido', 'dni', 'foto', 'telefono', 'correo', 'fecha_ingreso', 'fecha_nacimiento', 'grado_academico']
        widgets = {'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombres', 'required':''}), 
        'apellido': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apellidos', 'required':''}),
        'dni' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'DNI'}), 
        'telefono' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Celular', 'required':''}),
        'correo' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Correo electrónico', 'required':''}),
        'fecha_ingreso' : forms.TextInput(attrs={'class':'form-control', 'readonly':''}),
        'grado_academico' : forms.Select(attrs={'class':'form-control'}),
        }
        
class MiembrosRegistro(forms.ModelForm):
    class Meta:
        model = Miembros
        fields = ['nombre','apellido', 'dni', 'foto', 'telefono', 'correo', 'fecha_ingreso', 'fecha_nacimiento', 'grado_academico']
        widgets = {'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombres', 'required':'', 'autocomplete':'off'}), 
        'apellido': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Apellidos', 'required':'', 'autocomplete':'off'}),
        'dni' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'DNI', 'autocomplete':'off', 'required':''}), 
        'telefono' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Celular', 'required':'', 'autocomplete':'off'}),
        'correo' : forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Correo electrónico', 'required':'', 'autocomplete':'off'}),
        'grado_academico' : forms.Select(attrs={'class':'form-control', 'required':''}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']
        widgets = {'password' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder': '', 'required':''}), }
    
class RegistrarProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['codigo', 'nombre', 'descripcion', 'fecha_inicio', 'foto']
        widgets = {'codigo': forms.TextInput(attrs={'placeholder': 'Código del proyecto', 'required':''}), 
        'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del proyecto', 'required':''}),
        'descripcion' : forms.TextInput(attrs={'placeholder': 'Descripción'}),
        'fecha_inicio' : forms.DateInput(format=('%d-%m-%Y'), attrs={'placeholder':'Fecha de inicio del proyecto'})
        }
        
class CoordinadorProyectoForm(forms.ModelForm):
    class Meta:
        model = Miembro_Proyecto
        fields = ['idMiembro']
        labels = {'idMiembro': 'Coordinador',}
        widgets = {
            'idMiembro': forms.Select(attrs={'class':'form-control'}) 
        }
                
class MiembroProyectoForm(forms.ModelForm):
    class Meta:
        model = Miembro_Proyecto
        fields = ['idMiembro', 'idCargo', 'fecha_miembro_proyecto', 'descripcion']
        widgets = {
            'idCargo': forms.Select(attrs={'class':'form-control'}),
            'fecha_miembro_proyecto': DatePickerInput(format='%d/%m/%Y', attrs={'type': 'datepicker', 'name': 'fecha', 'class':'form-control datepicker','id':'fecha'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
        }
        
class Recurso_ProyectoForm(forms.ModelForm):
    class Meta:
        model = Recurso_Proyecto
        fields = ['idProyecto', 'idRecurso', 'fecha_recurso_proyecto', 'descripcion', 'estado']
        widgets = {
            'fecha_recurso_proyecto': DatePickerInput(format='%d/%m/%Y', attrs={'type': 'datepicker', 'name': 'fecha', 'class':'form-control datepicker','id':'fecha'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control'}),
        }

class Historial_RecursosForm(forms.ModelForm):
    class Meta:
        model = Historial_Recursos
        fields = ['fecha_historial', 'observaciones', 'idRecurso', 'idEstadoRecurso']

class EstadoRecursoForm(forms.ModelForm):
    class Meta:
        model = EstadoRecurso
        fields = ['descripcion']


class EntidadForm(forms.ModelForm):
    class Meta:
        model = Entidad
        fields = ['razon_social', 'ruc', 'telefono', 'correo', 'representante_legal']
        widgets = {
            'razon_social': forms.TextInput(attrs={'class':'form-control'}),
            'ruc': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'correo': forms.TextInput(attrs={'class':'form-control', 'type':'email'}),
            'representante_legal': forms.TextInput(attrs={'class':'form-control'}),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['codigo_documento', 'fecha_emision', 'tipo', 'ruta_pdf', 'estado', 'entidad']
        widgets = {
            'codigo_documento': forms.TextInput(attrs={'class':'form-control'}), 
            'fecha_emision': forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'form-control', 'id':'fecha', 'placeholder':'dd/mm/aaaa', 'type':'date'}),
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'entidad': forms.Select(attrs={'class':'form-control'}),
            'estado': forms.TextInput(attrs={'class':'form-control', 'value':'ACTIVO', 'readonly':''}),
            'ruta_pdf': forms.FileInput(attrs={'class':'form-control', 'accept':'application/pdf'}),
        }

class CargosForm(forms.ModelForm):
    class Meta:
        model = Cargos
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class':'form-control'})
            }

class ProyectosForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['codigo', 'nombre', 'descripcion', 'fecha_inicio']

class buscarProyectosForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['nombre']
        
class ProyectosEditForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['codigo', 'nombre', 'descripcion', 'fecha_inicio']
        widgets = { 'fecha_inicio': forms.DateInput(format=('%Y/%m/%d'), attrs={'class':'form-control', 'id':'llegada'})}


class Historial_ProyectoForm(forms.ModelForm):
    class Meta:
        model = Historial_Proyecto
        fields = ['fecha_historial', 'observaciones', 'idProyecto', 'idEstadoProyecto']


class EstadoProyectoForm(forms.ModelForm):
    class Meta:
        model = EstadoProyecto
        fields = ['descripcion']


class ResultadoProyectoForm(forms.ModelForm):
    class Meta:
        model = ResultadoProyecto
        fields = ['descripcion', 'fecha_resultado', 'idProyecto']


class Recurso_DocumentoForm(forms.ModelForm):
    class Meta:
        model = Recurso_Documento
        fields = ['idDocumento', 'idRecurso']
        widgets = {
            'idDocumento': forms.Select(attrs={'class':'form-control'}) 
        }

class Miembro_ProyectoForm(forms.ModelForm):
    class Meta:
        model = Miembro_Proyecto
        fields = ['idProyecto', 'idMiembro', 'idCargo', 'fecha_miembro_proyecto', 'descripcion', 'estado_miembro_proyecto']

class MiembroProyecto_RecursoProyectoForm(forms.ModelForm):
    class Meta:
        model = MiembroProyecto_RecursoProyecto
        fields = ['observacion', 'estado', 'fecha', 'idMiembro_Proyecto', 'idRecurso_Proyecto']
        widgets = {
            'idMiembro_Proyecto': forms.Select(attrs={'class':'form-control'}),
             'idRecurso_Proyecto': forms.Select(attrs={'class':'form-control'}),
             'observacion': forms.Textarea(attrs={'class':'form-control', 'rows':'5'}),
             'fecha': forms.DateTimeInput(attrs={'class':'form-control'})
        }
