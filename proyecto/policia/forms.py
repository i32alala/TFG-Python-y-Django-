#encoding: utf-8

from django.forms import ModelForm, TextInput
from django import forms
from policia.models import Acto,Sala,Asiento,Etiqueta,Personas,Invitaciones,Organismo,ActoPersona,ActoSala,personaRol,PersonaOrganismo,personaRol
from django.contrib.admin import widgets


class FormularioContacto(forms.Form):
	class Meta:
		model = Personas
		email = forms.EmailField(label='Email')

		widget = {
			'personas' : forms.CheckboxSelectMultiple,
		}

#formulario insertar personas
class PersonaForm(ModelForm):
	#nombrePersona = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre '}))

	class Meta:
		model = Personas
		fields = ['nombrePersona','apellido','cargo','correo','idOrganismo']
		labels = {'nombrePersona':'Nombre Persona ','apellido':'Apellidos', 'cargo': 'Cargo','correo': 'Email', 'idOrganismo':'Organismo'}

"""
class PersonaForm(forms.Form):
	nombrePersona = forms.CharField(max_length=100)
	apellido = forms.CharField(max_length=100)
	cargo = forms.ModelChoiceField(queryset=personaRol.objects.all())
	correo = forms.EmailField()
	
"""

#formulario enviar email
class UnknownForm(forms.Form):
	
	class Meta:
		model = Acto,Invitaciones
		
#Formulario insertar y editar asientos		
class AsientoForm(ModelForm):
	class Meta:
		model = Asiento
		fields = ['numAsiento','filaAsiento','columnaAsiento','idSala']
		labels = {"numAsiento":"Número del asiento","filaAsiento":"Fila","columnaAsiento":"Columna","idSala":"Sala"}

#formularioRoles (protocolo)		
class PersonaRolForm(ModelForm):
	class Meta:
		model = personaRol
		fields=['rol','orden']
		labels = {"rol":"Cargo", "orden":"Prioridad" }

		
#Formulario salas 
class SalaForm(ModelForm):
	class Meta:
		model = Sala
		fields = ['nombreSala','idSala','numFilas','numColumnas','numAsientos','descripcionSala','imagenSala']
		labels = {"idSala":"Numero de sala","nombreSala" : "Nombre de la sala", "numAsientos" : "Número de Asientos", "descripcionSala" : "Descripción de la sala", "imagenSala" : "Foto","numFilas":"Número de filas", "numColumnas": "Número de columnas"}

	
#Formulario etiquetas
class EtiquetaForm(ModelForm):
	class Meta:
		model = Etiqueta
		fields = ['nombreEtiqueta','parteAbajo','parteArriba','gorro','zapatos','corbata','chaqueta','jersey']
		labels = {"nombreEtiqueta": "Nombre", "parteAbajo": "Pantalón", "parteArriba":"Parte de Arriba", "gorro":"Gorro", "zapatos" : "Zapatos", "corbata":"Corbata", "medias":"Medias", "cinturon":"Cinturón", "bolso":"Bolso", "falda":"Falda", "chaqueta":"Chaqueta","jersey":"Jersey"}

#Formulario para los organismos
class OrganismoForm(ModelForm):
	class Meta:
		model = Organismo
		fields = ['nombreOrganismo']
		labels = {"nombreOrganismo" : "Nombre del organismo"}
		
#Formulario para insertar y editar invitaciones
class InvitacionForm(ModelForm):
	class Meta:
		model = Invitaciones
		fields =['idActo','nombreInvitacion']
		labels = {"idActo":"Acto","nombreInvitacion":"Nombre de la invitación"}
		
#formulario para insertar y editar actos
class ActoForm(forms.ModelForm):
	class Meta:
		model = Acto
		fields = ['nombreActo','fechaActo','descripcionActo','idSala','idEtiqueta']
		labels = {"nombreActo": "Nombre del Acto", "fechaActo" : "Fecha del Acto", "descripcionActo":"Descripción", "idSala": "Sala donde se reliza el Acto", "idEtiqueta":"Etiqueta elegida"}
		#widgets = {
		#	'person': forms.CheckboxSelectMultiple
		#}

#Formulario para insertar en la tabla intermedia entre actos y salas
class actoSalaForm(forms.ModelForm):
	class Meta:
		model = ActoSala
		fields = ['acto','idSala']

#Formulario para insertar tabla intermedia entre organismos y personas		
class organismoPersona(forms.ModelForm):
	class Meta:
		model = PersonaOrganismo
		fields = ['idOrganismo','idPersona','cargo']

#Formulario para insertar en la tabla intermedia de actos y personas
class invitacionPersForm(forms.ModelForm):
	class Meta:
		model = ActoPersona
		fields = ['acto', 'person','asistencia','orden']


