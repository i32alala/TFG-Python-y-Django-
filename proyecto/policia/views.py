from django.shortcuts import render,render_to_response, get_object_or_404
from django.http import Http404
from .models import Acto,Sala,Asiento,Etiqueta,Invitaciones,Organismo,Personas,ActoPersona,Noticia,Tag,ActoSala,personaRol,PersonaOrganismo
from .forms import SalaForm,FormularioContacto, ActoForm, EtiquetaForm, UnknownForm,InvitacionForm, OrganismoForm, PersonaForm, invitacionPersForm,actoSalaForm,organismoPersona,AsientoForm,PersonaRolForm,AsientoForm
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.mail import send_mail,EmailMessage
from io import BytesIO
#from reportlab.pdfgen import canvas
from django.views.generic import View
from django.core.mail import send_mail, get_connection
from smtplib import SMTP
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.shortcuts import redirect
from email.MIMEMultipart import MIMEMultipart
from email.Encoders import encode_base64
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.views.generic import ListView
#from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
#from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.lib import colors
#from reportlab.lib.pagesizes import letter
#from reportlab.platypus import Table
from django.db.models import Q
from django.core.paginator import Paginator
from itertools import chain
from django.views.defaults import page_not_found

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Vista para mostrar detalles de las salas
         
@login_required(login_url='/ingresar')
def salas_detail(request, nombreSala):
	try:
		detalleSalas = Sala.objects.get(idSala=nombreSala) #pasamos la sala elegida
		asientos = Asiento.objects.filter( idSala = nombreSala)
	except Sala.DoesNotExist:
		raise Http404("Salas no hay")
	return render_to_response('policia/detalleSalas.html', {'detalleSalas': detalleSalas,'asientos':asientos})


#Vista para mostrar las personas confirmadas y la prioridad (orden) que tienen
	
def ubi(request, ubI):
    noticias = Acto.objects.get(idActo = ubI)
    tags = Personas.objects.all()
    confirmadas = ActoPersona.objects.filter(acto = ubI).order_by("orden")
    
    return render_to_response('policia/ubicac.html', {'noticias':noticias, 'tags':tags, 'confirmadas':confirmadas}, context_instance=RequestContext(request))
    

#Elegimos a las personas de un organismo concreto
#para invitarlas a un acto concreto
 	
def invPers(request, act):
	actos = Acto.objects.get(idActo = act)
	personas = PersonaOrganismo.objects.all()
	confirmadas = ActoPersona.objects.filter(acto = act)
	organismos = Organismo.objects.all()
	personas = Personas.objects.all()
	
	return render_to_response('policia/invPers.html', {'actos':actos, 'personas':personas, 'confirmadas':confirmadas,'organismos':organismos}, context_instance=RequestContext(request))



#Con esta vista sentamos a las personas en su asiento correspondiente
    
def ubi2(request, ubI,idS):
    noticias = Acto.objects.get(idActo = ubI)
    tags = ActoPersona.objects.filter(acto = ubI)
    count = ActoPersona.objects.filter(acto = ubI).order_by("orden").count()
    confirmadas = ActoPersona.objects.filter(acto = ubI).order_by("orden")
    asientos = Asiento.objects.filter(idSala = idS).order_by("numAsiento","-columnaAsiento")[:count]
    salas = ActoSala.objects.filter(acto = ubI)
    sal = Sala.objects.get(idSala = idS)
    
    i=0
    for x in confirmadas:
    	if x.asistencia == 1:
    		x.numAsiento 		= asientos[i].numAsiento
    		x.filaAsiento 		= asientos[i].filaAsiento
    		x.columnaAsiento 	= asientos[i].columnaAsiento
    		i += 1
    
    return render_to_response('policia/sentarAsis.html', {'noticias':noticias, 'tags':tags, 'confirmadas':confirmadas, 'salas': salas, 'asientos':asientos,'sal':sal}, context_instance=RequestContext(request))
    

#seleccionamos (elegimos) a las personas de un organismo concreto para invitarlas
    
def personActo(request, org,act):
	acto = Acto.objects.get(idActo = act)
	organismo = Organismo.objects.get(idOrganismo = org)
	personas = Personas.objects.filter(idOrganismo = org)
	confirmadas = ActoPersona.objects.filter(acto = act)

	
	return render_to_response('policia/detOrganismo.html', {'acto':acto,'confirmadas':confirmadas, 'organismo':organismo,'personas':personas}, context_instance=RequestContext(request))

def prueba(request, idA):
    noticias = Acto.objects.get(idActo = idA)
    tags = Personas.objects.all()
    confirmadas = ActoPersona.objects.filter(acto = idA)
    
    return render_to_response('policia/consulta.html', {'noticias':noticias, 'tags':tags, 'confirmadas':confirmadas}, context_instance=RequestContext(request))

#Mostramos los detalles de un acto
@login_required(login_url='/ingresar')
def actosDetail(request, idA):
	detalleActo = Acto.objects.get(idActo = idA)
	personaActo = Personas.objects.all()
	confirmadas = ActoPersona.objects.filter(acto = idA)

	return render_to_response('policia/detalleActos.html', {'detalleActo': detalleActo, 'personaActo':personaActo, 'confirmadas':confirmadas})
	
#Mostramos los detalles de una persona	
@login_required(login_url='/ingresar')
def personaDetail(request, idP):
	personas = Personas.objects.get(idPersona = idP)
	

	return render_to_response('policia/detallePersonas.html', {'personas': personas})
	
#Enviar emails a las personas con mensajes de texto y ficheros
def sendEmail(request):

	print request

	if request.method == 'POST':
		form = UnknownForm(request.POST, request.FILES)
		print form
		if form.is_valid():
			if 'enviar' in request.POST:
				for value in request.POST.getlist('choices'):
					asunto = request.POST['asunto']
					mensaje = request.POST['mensaje']
					files = request.FILES['file']
					mail = EmailMessage(asunto, mensaje, to =[value])
					mail.attach(files.name, files.read(), files.content_type)
				
					mail.send()
				return HttpResponseRedirect('/policia/actosInvita')
				
		else:
			form = UnknownForm()
		return render_to_response('policia/invitacionesenviar.html', context_instance=RequestContext(request))
					
				

@login_required(login_url='/ingresar')
def consultaActo(request):
	acto = ActoPersona.objects.all()

	context = {'acto':acto}
	return render(request, "policia/consulta.html", context)

#Ver invitaciones
@login_required(login_url='/ingresar')
def invitacion(request):
	invitacion = Invitaciones.objects.all()
	return render_to_response('policia/invitaciones.html', {'invitacion':invitacion})

#Ver salas paginadas
@login_required(login_url='/ingresar')
def salas(request):
	salas = Sala.objects.all()
	
	paginator = Paginator(salas, 10)
	
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		salas = paginator.page(page)
	except(EmptyPage, InvalidPage):
		salas = paginator.page(paginator.num_pages)
		
	
	return render_to_response('policia/salas.html', {'salas':salas})

#ver Organismos paginados
@login_required(login_url='/ingresar')
def organismos(request):
	organismos = Organismo.objects.all()
	
	paginator = Paginator(organismos, 10)
	
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		organismos = paginator.page(page)
	except(EmptyPage, InvalidPage):
		organismos = paginator.page(paginator.num_pages)
		
	return render_to_response('policia/organismos.html', {'organismos':organismos})

@login_required(login_url='/ingresar')
def persona(request):
	persona = Personas.objects.all()
	return render_to_response('policia/personas.html',{'persona':persona},)

#ver personas paginadas
@login_required(login_url='/ingresar')
def mostrarPersona(request):
	mostrarpersona = Personas.objects.all()
	
	paginator = Paginator(mostrarpersona, 10)
	
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		mostrarpersona = paginator.page(page)
	except(EmptyPage, InvalidPage):
		mostrarpersona = paginator.page(paginator.num_pages)
	
	return render_to_response('policia/mostrarPersona.html', {'mostrarpersona':mostrarpersona})

#borrar personas	
@login_required(login_url='/ingresar')
def borrarPersona(request, bPer):
	borrarPersonas = Personas.objects.get(idPersona = bPer)
	borrarPersonas.delete()

	return HttpResponseRedirect('/policia/mostrarPersonas',{'borrarPersonas':borrarPersonas})

#borrar Asientos
@login_required(login_url='/ingresar')
def borrarAsiento(request, bAs):
	borrarAsientos = Asiento.objects.get(idAsiento = bAs)
	borrarAsientos.delete()

	return HttpResponseRedirect('/policia/salas',{'borrarAsientos':borrarAsientos})

#borrar Roles	
@login_required(login_url='/ingresar')
def borrarRoles(request, bRol):
	borrarRoles = personaRol.objects.get(idRol = bRol)
	borrarRoles.delete()

	return HttpResponseRedirect('/policia/roles',{'borrarRoles':borrarRoles})

#ver detalles personas
@login_required(login_url='/ingresar')
def personaDetalle(request, perdet):
	detalPersona = Personas.objects.get(idPersona = perdet)
	return render_to_response('policia/detallePersona.html', {'detalPersona':detalPersona})

#ver etiquetas paginadas
@login_required(login_url='/ingresar')
def etiqueta(request):
	etiquetas = Etiqueta.objects.all()
	
	paginator = Paginator(etiquetas, 10)
	
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		etiquetas = paginator.page(page)
	except(EmptyPage, InvalidPage):
		etiquetas = paginator.page(paginator.num_pages)

	return render_to_response('policia/etiquetas.html',{'etiquetas':etiquetas})

#ver roles paginados
@login_required(login_url='/ingresar')
def personaRoles(request):
	rol = personaRol.objects.all()
	
	paginator = Paginator(rol, 10)
	
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		rol = paginator.page(page)
	except(EmptyPage, InvalidPage):
		rol = paginator.page(paginator.num_pages)

	return render_to_response('policia/roles.html',{'rol':rol})

#ver detalles etiquetas
@login_required(login_url='/ingresar')
def etiquetaDetail(request, idE):
	detalleEtiqueta = Etiqueta.objects.get(idEtiqueta = idE)
	return render_to_response('policia/detalleEtiqueta.html', {'detalleEtiqueta': detalleEtiqueta})

#editar invitaciones
@login_required(login_url='/ingresar')
def editInvitacion(request, idin):
	editInvitacion = Invitaciones.objects.get(idInvitaciones=idin)
	if request.method == 'POST':
		form = InvitacionForm(request.POST, request.FILES, instance = editInvitacion)
		if form.is_valid():
			formulario = form.save(commit=False)
			formulario.save()

			return HttpResponseRedirect('/policia/invitaciones')
	else:
		form = InvitacionForm(instance=editInvitacion)
	context = {'form':form}
	return render(request, 'policia/editinvitaciones.html',context)

#editar Organismos
@login_required(login_url='/ingresar')	
def editOrganismo(request, idor):
	editOrganism = Organismo.objects.get(idOrganismo=idor)
	if request.method == 'POST':
		form = OrganismoForm(request.POST, instance = editOrganism)
		if form.is_valid():
			formulario = form.save(commit=False)
			formulario.save()

			return HttpResponseRedirect('/policia/organismos')
	else:
		form = OrganismoForm(instance=editOrganism)
	context = {'form':form}
	return render(request, 'policia/editOrganismos.html',context)

#editar Asientos
@login_required(login_url='/ingresar')
def editAsiento(request, idas):
	editAsi = Asiento.objects.get(idAsiento=idas)
	if request.method == 'POST':
		form = AsientoForm(request.POST, instance = editAsi)
		if form.is_valid():
			formulario = form.save(commit=False)
			formulario.save()

			return HttpResponseRedirect('/policia/salas')
	else:
		form = AsientoForm(instance=editAsi)
	context = {'form':form}
	return render(request, 'policia/editAsientos.html',context)
	
#editar salas
@login_required(login_url='/ingresar')
def editSalas(request, idS):
	editSala = Sala.objects.get(idSala=idS)
	if request.method == 'POST':
		form = SalaForm(request.POST,request.FILES, instance = editSala)
		if form.is_valid():
			formulario = form.save(commit=False)
			formulario.save()

			return HttpResponseRedirect('/policia/salas')
	else:
		form = SalaForm(instance=editSala)
	context = {'form':form}
	return render(request, 'policia/editarSala.html',context)

#editar actos	
@login_required(login_url='/ingresar')
def editActos(request, idac):
	idActo = ""
	editActo = Acto.objects.get(idActo=idac)
	if request.method == 'POST':
		formulario = ActoForm(request.POST, instance = editActo)
		if formulario.is_valid():
			idActo = formulario.save()
			for x in request.POST.getlist('person'):
				form = invitacionPersForm({'acto':str(idActo.pk), 'person':x, 'orden':-1})
				form.save()
			return HttpResponseRedirect('/policia/actos')
	else:
		formulario = ActoForm(instance=editActo)
	context = {'formulario':formulario}
	return render(request, 'policia/editactos.html',context)

#insertar actos nuevos	
@login_required(login_url='/ingresar')
def nuevoActo(request):
	idActo = ""
	idSala = ""
	if request.method=='POST':
		formulario = ActoForm(request.POST, request.FILES)
		if formulario.is_valid():
			idActo = formulario.save()
			idSala = formulario.save()
#			for x in request.POST.getlist('person'):
#				form = invitacionPersForm({'acto': str(idActo.pk), 'person': x, 'orden':-1})
#				form.save()
			for i in request.POST.getlist('idSala'):
				formu = actoSalaForm({'acto': str(idActo.pk), 'idSala': i})
				formu.save()			
			
			return HttpResponseRedirect('/policia/actos/')
	else:
		formulario = ActoForm()
	return render_to_response('policia/actoform.html',{'formulario':formulario}, context_instance=RequestContext(request))

#insertar nuevas personas
@login_required(login_url='/ingresar')
def nuevaPersona(request):
	idPersona = ""
	if request.method=='POST':
		formulario = PersonaForm(request.POST, request.FILES)
		if formulario.is_valid():
			idPersona = formulario.save()
			for x in request.POST.getlist('idOrganismo'):
				form = organismoPersona({'idOrganismo': x, 'idPersona':str(idPersona.pk), 'cargo': idPersona.cargo, 'nombreOrganismo': idPersona.idOrganismo.nombreOrganismo})
				form.save()
			
			return HttpResponseRedirect('/policia/mostrarPersonas/')
	else:
		formulario = PersonaForm()
	return render_to_response('policia/personaform.html',{'formulario':formulario}, context_instance=RequestContext(request))
	
#editar personas	
@login_required(login_url='/ingresar')
def editPersonas(request, idpe):
	editPersona = Personas.objects.get(idPersona=idpe)
	if request.method == 'POST':
		form = PersonaForm(request.POST, request.GET, instance = editPersona)
		if form.is_valid():
			formulario = form.save(commit=False)
			formulario.save()

			return HttpResponseRedirect('/policia/mostrarPersonas')
	else:
		form = PersonaForm(instance=editPersona)
	context = {'form':form}
	return render(request, 'policia/editPersona.html',context)
	
	
#editar etiquetas	
@login_required(login_url='/ingresar')
def editEtiquetas(request, idet):
	editEtiqueta = Etiqueta.objects.get(idEtiqueta=idet)
	if request.method == 'POST':
		form = EtiquetaForm(request.POST, request.GET, instance = editEtiqueta)
		if form.is_valid():
			formulario = form.save(commit=False)
			formulario.save()

			return HttpResponseRedirect('/policia/etiquetas')
	else:
		form = EtiquetaForm(instance=editEtiqueta)
	context = {'form':form}
	return render(request, 'policia/editEtiqueta.html',context)
	
#editar roles	
@login_required(login_url='/ingresar')
def editRoles(request, idrol):
	editRol = personaRol.objects.get(idRol=idrol)
	if request.method == 'POST':
		form = PersonaRolForm(request.POST, request.GET, instance = editRol)
		if form.is_valid():
			formulario = form.save(commit=False)
			formulario.save()

			return HttpResponseRedirect('/policia/roles')
	else:
		form = PersonaRolForm(instance=editRol)
	context = {'form':form}
	return render(request, 'policia/editRoles.html',context)


#ver detalles invitaciones
@login_required(login_url='/ingresar')
def invitacionDetail(request, idInvitaciones):
	detalleInvitacion = Invitaciones.objects.get(idInvitaciones=idInvitaciones)
	return render_to_response('policia/detalleInvitaciones.html', {'detalleInvitacion': detalleInvitacion})

#ver actos paginados
@login_required(login_url='/ingresar')
def actos(request):
	actos = Acto.objects.all()
	salas = Sala.objects.all()
	
	paginator = Paginator(actos, 10)
	
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		actos = paginator.page(page)
	except(EmptyPage, InvalidPage):
		actos = paginator.page(paginator.num_pages)
		
	return render_to_response('policia/actos.html', {'actos': actos, 'salas':salas})
	
#vista para insertar personas en tabla intermedia entre actos y personas al pulsar sobre invitar personas
def incluir(request):				
	if request.method=='POST':
			
			if 'enviar' in request.POST:
				
				for x in request.POST.getlist('personas'):
					
					act = request.POST['acto']
					form = invitacionPersForm({'acto': act,'person': x, 'orden': -1})
					if form.is_valid():
						form.save()

					
				return HttpResponseRedirect('/policia/actos')
	else:
		formulario = invitacionPersForm()
	return render_to_response('policia/detOrganismo.html', {'formulario':formulario}, context_instance=RequestContext(request))

#insertar orden manual en personas confirmadas
@login_required(login_url='/ingresar')
def generarOrden(request, acto_id):
	actoPersona = ActoPersona.objects.filter(acto = acto_id, asistencia = 1)
	for x in actoPersona: 
		if x.person.cargo.orden:
			acto = ActoPersona.objects.filter(acto = acto_id, person = x.person, asistencia = 1)
			acto.update(orden = x.person.cargo.orden)
			
	return HttpResponseRedirect('/policia/actos')			
		

@login_required(login_url='/ingresar')
def nuevoActoPersona(request):
	actoPersona = ActoPersona.objects.get(acto = request.POST['acto'],person = request.POST['person'])
	actoPersona.asistencia = request.POST.get("asistencia",False)

			
	if request.method=='POST':
		formulario = invitacionPersForm(request.POST,instance=actoPersona)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/policia/actos')
	else:
		formulario = invitacionPersForm()
	return render_to_response('policia/actoPersonaForm.html', {'formulario':formulario}, context_instance=RequestContext(request))
	
#vista para aplicar el protocolo	
@login_required(login_url='/ingresar')
def nuevoOrden(request):
	actoPersona = ActoPersona.objects.get(acto = request.POST['acto'],person = request.POST['person'])
	actoPersona.asistencia = request.POST.get("asistencia",False)
	actoPersona.orden = request.POST.get("orden")
	
	print actoPersona.asistencia
		
	if request.method=='POST':
		formulario = invitacionPersForm(request.POST,instance=actoPersona)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/policia/actos')
	else:
		formulario = invitacionPersForm()
	return render_to_response('policia/actoPersonaForm.html', {'formulario':formulario}, context_instance=RequestContext(request))

#insertar nuevo organismo
@login_required(login_url='/ingresar')
def nuevoOrganismo(request):
	if request.method=='POST':
		formulario = OrganismoForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/policia/organismos/')
	else:
		formulario = OrganismoForm()
	return render_to_response('policia/organismoform.html',{'formulario': formulario}, context_instance=RequestContext(request))

#insertar nuevo rol
@login_required(login_url='/ingresar')
def nuevoRol(request):
	if request.method=='POST':
		form = PersonaRolForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/policia/roles/')
	else:
		form = PersonaRolForm()
	return render_to_response('policia/rolform.html',{'form': form}, context_instance=RequestContext(request))

#insertar nueva etiqueta
@login_required(login_url='/ingresar')
def nuevaEtiqueta(request):
	if request.method=='POST':
		formulario = EtiquetaForm(request.POST, request.FILES)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/policia/etiquetas/')
	else:
		formulario = EtiquetaForm()
	return render_to_response('policia/etiquetaform.html',{'formulario':formulario}, context_instance=RequestContext(request))


#insertar nueva sala

@login_required(login_url='/ingresar')
def salaNueva(request):
	if request.method=='POST':
		formulario = SalaForm(request.POST, request.FILES)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/policia/salas')
	else:
		formulario = SalaForm()
	return render_to_response('policia/salaform.html',{'formulario':formulario}, context_instance=RequestContext(request))
	
#insertar nuevo asiento	
@login_required(login_url='/ingresar')
def AsientoNuevo(request):
	if request.method=='POST':
		formulario = AsientoForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/policia/salas')
	else:
		formulario = AsientoForm()
	return render_to_response('policia/asientoform.html',{'formulario':formulario}, context_instance=RequestContext(request))

#insertar nueva invitacion
@login_required(login_url='/ingresar')
def nuevaInvitacion(request):
	if request.method=='POST':
		formulario = InvitacionForm(request.POST, request.FILES)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/policia/invitaciones')
	else:
		formulario = InvitacionForm()
	return render_to_response('policia/invitacionesform.html', {'formulario': formulario}, context_instance=RequestContext(request))

#ver asientos
@login_required(login_url='/ingresar')
def verAsientos(request, sal):
	salas = Sala.objects.get(idSala = sal)
	asientos = Asiento.objects.filter(idSala = sal).order_by("numAsiento")
	
	paginator = Paginator(asientos, 20)
	
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		asientos = paginator.page(page)
	except(EmptyPage, InvalidPage):
		asientos = paginator.page(paginator.num_pages)
	
	return render_to_response('policia/verAsientos.html', {'salas': salas, 'asientos': asientos})


#@login_required(login_url='/ingresar')
#def borrarAsiento(request, asi):
#	borrarAsiento = Asiento.objects.get(idAsiento = asi)
#	borrarAsiento.delete()
#
#	return HttpResponseRedirect('/policia/salas',{'borrarAsiento':borrarAsiento})
	
#borrar salas
@login_required(login_url='/ingresar')
def borrarSala(request, Sal):
	borrarSalas = Sala.objects.get(idSala = Sal)
	borrarSalas.delete()

	return HttpResponseRedirect('/policia/salas',{'borrarSalas':borrarSalas})

#borrar actos
def borrarActo(request, Act):
	borrarActos = Acto.objects.get(idActo = Act)
	borrarActos.delete()

	return HttpResponseRedirect('/policia/actos',{'borrarActos':borrarActos})
	
#borrarInvitaciones
def borrarInvitacionespitosas(request, inviTa):
	borrarInvitacionespitosas = Invitaciones.objects.get(idInvitaciones = inviTa)
	borrarInvitacionespitosas.delete()
	
	return HttpResponseRedirect('/policia/invitaciones',{'borrarInvitacionespitosas':borrarInvitacionespitosas})

#borrarInvitaciones
@login_required(login_url='/ingresar')
def borrarInvitacion(request, invit):
	invitacionesb = Invitaciones.objects.get(idInvitaciones=invit)
	invitacionesb.delete()

	return HttpResponseRedirect('/policia/invitaciones',{'invitacionesb':invitacionesb})

#borrar etiquetas
@login_required(login_url='/ingresar')
def borrarEtiqueta(request, Etiq):
	borrarEtiquetas = Etiqueta.objects.get(idEtiqueta = Etiq)
	borrarEtiquetas.delete()

	return HttpResponseRedirect('/policia/etiquetas', {'borrarEtiquetas':borrarEtiquetas})

#borrar Organismo
@login_required(login_url='/ingresar')
def borrarOrganismo(request, Org):
	borrarOrganismo = Organismo.objects.get(idOrganismo = Org)
	borrarOrganismo.delete()

	return HttpResponseRedirect('/policia/organismos',{'borrarOrganismo':borrarOrganismo})

#login
def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/policia/privado')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/policia/privado')
				else:
					return render_to_response('usuarios/noactivo.html',context_instance=RequestContext(request))
			else:
				return render_to_response('usuarios/nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('usuarios/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def actosInvitaciones(request):
	actosInvita = Acto.objects.all()

	return render_to_response('policia/enviarInvitaciones.html', {'actosInvita': actosInvita})


#ver peronas invitadas a un acto concreto
@login_required(login_url='/ingresar')
def actosDetailInvitaciones(request, idA):
	actos = Acto.objects.get(idActo = idA)
	personas = Personas.objects.all()
	confirmadas = ActoPersona.objects.filter(acto = idA)

	return render_to_response('policia/detalleActosInvitaciones.html', {'actos': actos, 'personas':personas, 'confirmadas':confirmadas}, context_instance=RequestContext(request))

#ver pag principal
@login_required(login_url='/ingresar')
def privado(request):
	usuario = request.user
	return render_to_response('policia/content.html',{'usuario':usuario}, context_instance=RequestContext(request))

#deslogueo
@login_required(login_url='/ingresar')
def deslogueo(request):
	logout(request)
	return HttpResponseRedirect('/')
