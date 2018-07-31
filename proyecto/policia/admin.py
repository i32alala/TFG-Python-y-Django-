from django.contrib import admin
from .models import Acto,Sala,Asiento,Etiqueta,Invitaciones,Organismo,Personas,ActoPersona,PersonaOrganismo,personaRol,Noticia,Tag,ActoSala

# Register your models here.

admin.site.register(Acto)
admin.site.register(Sala)
admin.site.register(Asiento)
admin.site.register(Etiqueta)
admin.site.register(Invitaciones)
admin.site.register(Organismo)
admin.site.register(Personas)
admin.site.register(ActoPersona)
admin.site.register(PersonaOrganismo)
admin.site.register(Noticia)
admin.site.register(Tag)
admin.site.register(personaRol)
admin.site.register(ActoSala)
