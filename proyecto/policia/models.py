from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Etiqueta(models.Model):
	idEtiqueta = models.AutoField(primary_key=True)
	nombreEtiqueta = models.CharField(max_length=200)
	parteAbajo = models.CharField(max_length=200)
	parteArriba = models.CharField(max_length = 200)
	gorro = models.CharField(max_length = 200)
	zapatos = models.CharField(max_length = 200)
	corbata = models.CharField(max_length = 200)
	medias = models.CharField(max_length = 200)
	cinturon = models.CharField(max_length = 200)
	bolso = models.CharField(max_length = 200)
	falda = models.CharField(max_length = 200)
	chaqueta = models.CharField(max_length = 200)
	jersey = models.CharField(max_length = 200)

	def __str__(self):
		return self.nombreEtiqueta
		return self.parteAbajo
		return self.parteArriba
		return self.gorro
		return self.zapatos
		return self.corbata
		return self.medias
		return self.cinturon
		return self.bolso
		return self.falda
		return self.chaqueta
		return self.jersey

class Sala(models.Model):
	idSala = models.IntegerField(primary_key=True)
	nombreSala = models.CharField(max_length=200, help_text="Introduzca el nombre de la sala")
	numAsientos = models.IntegerField(default=0)
	descripcionSala = models.CharField(max_length=200,help_text="Descriva brevemente el acto")
	imagenSala = models.ImageField(upload_to='img', blank = True, null = True)
	media = models.FileField(upload_to='archivos/', blank=True,null =True)
	numFilas = models.IntegerField(null = True)
	numColumnas = models.IntegerField(null= True)

	def __str__(self):
		return str(self.idSala)
		return self.nombreSala
		return self.descripcionSala
		return self.media
		return self.imagenSala
		return self.numFilas
		return self.numColumnas
		
class Organismo(models.Model):
	idOrganismo = models.AutoField(primary_key=True)
	nombreOrganismo = models.CharField(max_length = 200, null = False)

	def __str__(self):
		return self.nombreOrganismo


class personaRol(models.Model):
	idRol = models.AutoField(primary_key=True)
	rol = models.CharField(max_length=200)
	orden = models.IntegerField(null = True)
	
	def __str__(self):
		return self.rol
	
	class Meta:
		unique_together = (("rol", "orden"),)
	

class Personas(models.Model):
	idPersona = models.AutoField(primary_key=True)
	nombrePersona = models.CharField(max_length = 200, null = False)
	apellido = models.CharField(max_length = 200, null = True)
	cargo = models.ForeignKey('personaRol', on_delete=models.SET_NULL, null=True)
	correo = models.EmailField()
	idOrganismo = models.ForeignKey('Organismo', on_delete=models.SET_NULL, null=True)


	def __str__(self):
		return self.nombrePersona
		return self.apellido
		return self.cargo
		return self.correo
		return self.idOrganismo



class Acto(models.Model):
	idActo = models.AutoField(primary_key=True)
	nombreActo = models.CharField(max_length=200)
	fechaActo = models.DateField(null=True, blank=True)
	descripcionActo = models.CharField(max_length=200)
	idSala = models.ForeignKey('Sala', on_delete=models.SET_NULL, null=True)
	idEtiqueta = models.ForeignKey('Etiqueta', on_delete=models.SET_NULL, null=True)
	#person = models.ManyToManyField('Personas')


	def __unicode__(self):
		return self.nombreActo
		return self.fechaActo
		return self.descripcionActo
		return self.idSala
		return self.idEtiqueta
		#return self.person


class ActoSala(models.Model):
	acto = models.ForeignKey(Acto)
	idSala = models.ForeignKey(Sala)
	
	class Meta:
		unique_together = (("acto", "idSala"),)
	
class ActoPersona(models.Model):
	acto = models.ForeignKey(Acto)
	person = models.ForeignKey(Personas)
	orden = models.IntegerField(help_text = "Orden en la lista de protocolo", null = True, default="-1")
	asistencia = models.BooleanField(default=0)

	class Meta:
		unique_together = (("acto", "person"),)
	#idActoPersona = models.AutoField(primary_key=True)
	#actoNombre = models.CharField(max_length=9, help_text = "Orden en la lista de protocolo", null = True)

	#def __unicode__(self):
	#	return self.organismo




class Invitaciones(models.Model):
	idInvitaciones = models.AutoField(primary_key=True)
	nombreInvitacion = models.CharField(max_length = 200)
	pdf = models.FileField(upload_to='media/',blank=True, null=True)
	idActo = models.ForeignKey('Acto', on_delete=models.SET_NULL, null=True)
	archivo = models.FileField(upload_to='media/', blank=True,null =True)

	def __str__(self):
		return self.nombreInvitacion
		return self.archivo
		return self.idActo


	list_display = ('file_link')
	def file_link(self):
		if self.archivo:
			return "<a href='%s'>download</a>" % (self.archivo.url,)
		else:
			return "No attachment"
	file_link.allow_tags = True



class Asiento(models.Model):
	idAsiento = models.AutoField(primary_key=True)
	numAsiento = models.IntegerField(null = True)
	filaAsiento = models.IntegerField(default=0)
	columnaAsiento = models.IntegerField(null = True)
	idSala = models.ForeignKey('Sala', on_delete=models.SET_NULL, null=True)
	idActo = models.ForeignKey('Acto', on_delete=models.SET_NULL, blank=True, null=True)

	
	def __str__(self):
		return str(self.numAsiento)


class PersonaOrganismo(models.Model):
	idOrganismo = models.ForeignKey('Organismo', on_delete=models.SET_NULL, null = True)
	idPersona = models.ForeignKey('Personas', on_delete=models.SET_NULL, null = True)
	cargo = models.CharField(max_length=200, help_text = "Crargo de la persona en el Organismo", null = True)
	nombreOrganismo = models.CharField(max_length=200, help_text = "Crargo de la persona en el Organismo", null = True)



class Tag(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length = 50)

class Noticia(models.Model):
    titulo= models.CharField(max_length=30)
    tags = models.ManyToManyField(Tag)
