from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Usuario(User):
	idUsuario = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200, help_text="Introduzca el nombre")

	LOAD_USERS = (
		('A', 'Admin'),
		('U', 'Usuario Normal'),
	)

	tipo = models.CharField(max_length=1, choices=LOAD_USERS, blank=True, default='U')

	def __str__(self):
		return self.name


class Invitaciones(models.Model):
	nombreInvitacion = models.CharField(max_length = 200, help_text="Introduzca el nombre de la invitacion", null= True)
	idInvitaciones = models.AutoField(primary_key = True)
	archivo = models.FileField(upload_to='archivos/', blank=True,null =True)
	pdf = models.FileField(upload_to='archivos/',blank=True, null=True)

	def __str__(self):
		return self.nombreInvitacion



class Sala(models.Model):
	idSala = models.AutoField(primary_key=True)
	nombreSala = models.CharField(max_length=200, help_text="Introduzca el nombre de la sala")
	numAsientos = models.IntegerField(default=0)
	descripcionSala = models.CharField(max_length=200,help_text="Descriva brevemente el acto")
	imagenSala = models.ImageField(upload_to='archivos/imagenes', blank = True, null = True)
	media = models.FileField(upload_to='archivos/', blank=True, null=True)

	def __str__(self):
		return self.nombreSala
		return self.descripcionSala
		return self.imagenSala


class Acto(models.Model):
	idActo = models.AutoField(primary_key=True)
	nombreActo = models.CharField(max_length=200, help_text="Introduzca el nombre del acto")
	fechaActo = models.DateField(null=True, blank=True)
	descripcionActo = models.CharField(max_length=200,help_text="Descriva brevemente el acto")
	idUsuario = models.ForeignKey('Usuario',on_delete=models.SET_NULL, null=True)
	idSala = models.ForeignKey('Sala', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.nombreActo
		return '%s ' % (self.usuario.idUsuario)
		return self.fechaActo
		return self.descripcionActo


class Asiento(models.Model):
	idAsiento = models.AutoField(primary_key=True)
	refAsiento = models.CharField(max_length=20, help_text="Asiento")
	filaAsiento = models.IntegerField(default=0)
	idSala = models.ForeignKey('Sala', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.refAsiento
		return self.filaAsiento

class Autoridad(models.Model):
	idAutoridad = models.AutoField(primary_key = True)
	nombre = models.CharField(max_length = 200, help_text = "Nombre Autoridad")
	tipo = models.CharField(max_length = 200, help_text = "Tipo Autoridad")

	LOAD_ASISTENCIA = (
		('S', 'Si'),
		('N', 'No'),
	)

	asistencia = models.CharField(max_length=1, choices=LOAD_ASISTENCIA, blank=True)
	idActo = models.ForeignKey('Acto', null = True)

	def __str__(self):
		return self.nombre
		return self.tipo
		return self.asistencia

class Organismo(models.Model):
	idOrganismo = models.AutoField(primary_key = True)
	nombre = models.CharField(max_length = 200, help_text="Nombre Organismo", null = True)
	idAutoridad = models.ForeignKey('Autoridad', null = True)

	def __str__(self):
		return self.nombre
		return self.idAutoridad

class Personas(models.Model):
	idPersona = models.AutoField(primary_key = True)
	nombre = models.CharField(max_length = 200, help_text = "Nombre Persona", null = False)
	apellido = models.CharField(max_length = 200, help_text ="Apellido Persona", null = True)
	cargo = models.CharField(max_length = 200, help_text="Cargo Persona", null = False)
	correo = models.EmailField(help_text='Email')
	idOrganismo = models.ForeignKey('Organismo', null = True)

	def __str__(self):
		return self.nombre
		return self.apellido
		return self.cargo
		return self.correo


class Etiqueta(models.Model):
	idEtiqueta = models.AutoField(primary_key=True)
	nombreEtiqueta = models.CharField(max_length=200, help_text = "Nombre etiqueta")
	parteAbajo = models.CharField(max_length=200, help_text = "Parte de abajo del traje")
	parteArriba = models.CharField(max_length = 200, help_text = "Parte de arriba del traje")
	gorro = models.CharField(max_length = 200, help_text = "Gorro")
	idAutoridad = models.ForeignKey('Autoridad', null = True)

	def __str__(self):
		return self.nombreEtiqueta
		return self.parteAbajo
		return self.parteArriba
		return self.gorro
