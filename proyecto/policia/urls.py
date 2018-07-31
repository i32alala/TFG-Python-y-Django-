from django.conf.urls import url
#from django_downloadview import ObjectDownloadView
#from policia.download.models import Invitaciones
from .import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import*
import django.views.defaults

#from policia.views import DescargarArchivoView

app_name = "policia"

#download = ObjectDownloadView.as_view(model=Document, file_field='file')

urlpatterns = [
	url(r'^$', views.ingresar, name='index'),
	url(r'^salas/$', views.salas, name='salas'),
	url(r'^salasDetail/(?P<nombreSala>\d+)/detail/$',views.salas_detail,name='sala-detail'),
	url(r'^actoDetail/(?P<idA>\d+)/detail/$', views.actosDetail, name='actoDetail'),
	url(r'^personaDetail/(?P<idP>\d+)/detail/$', views.personaDetail, name='personaDetail'),
	url(r'^actoDetailInv/(?P<idA>\d+)/detail/$', views.actosDetailInvitaciones, name='actoDetailInv'),
	url(r'^privado/$', views.privado, name='privado'),
	url(r'^cerrar/$', views.deslogueo, name='deslogueo'),
	url(r'^salasNuevas/$', views.salaNueva, name='nuevaSala'),
	url(r'^salas/(?P<Sal>\d+)/$', views.borrarSala, name='deleteSala'),
	#url(r'^asientos/(?P<asi>\d+)/$', views.borrarAsiento, name='deleteAsiento'),
#	url(r'^actoDetail/(?P<idInv>\d+)/$', views.borrarInvitado, name='borrarInvitado'),
	url(r'^editaSalas/(?P<idS>\d+)/$', views.editSalas, name='editSala'),
	url(r'^editaActos/(?P<idac>\d+)/$', views.editActos, name='editActo'),
	url(r'^editaPersonas/(?P<idpe>\d+)/$', views.editPersonas, name='editPersonas'),
	url(r'^editaInvitac/(?P<idin>\d+)/$', views.editInvitacion, name='editInvitacion'),
	url(r'^actos/$', views.actos, name='actos'),
	url(r'^actosInvita/$', views.actosInvitaciones, name='actosInvita'),
	url(r'^actos/(?P<Act>\d+)/$', views.borrarActo, name='deleteActo'),
	url(r'^roles/$',views.personaRoles, name='roles'),
	url(r'^roles/(?P<bRol>\d+)/$',views.borrarRoles, name='borrarRoles'),
	url(r'^actosNuevos/$', views.nuevoActo, name='nuevoActo'),
	url(r'^etiquetas/$', views.etiqueta, name='etiqueta'),
	url(r'^etiquetaDetail/(?P<idE>\d+)/detail/$',views.etiquetaDetail, name='etiquetaDetail'),
	url(r'^editaEtiquetas/(?P<idet>\d+)/$', views.editEtiquetas, name='editEtiqueta'),
	url(r'^editaRol/(?P<idrol>.+)/$',views.editRoles,name='editRol'),
	url(r'^editaOrganismo/(?P<idor>.+)/$',views.editOrganismo,name='editOrganismo'),
	url(r'^etiquetasNuevas/$', views.nuevaEtiqueta, name='nuevaEtiquet'),
	url(r'^etiquetas/(?P<Etiq>\d+)/$', views.borrarEtiqueta, name='deleteEtiqueta'),
	url(r'^invitaciones/$', views.invitacion, name='invitaciones'),
	#url(r'^invitaciones/(?P<idInvitaciones>\d+)/$', views.invitacionDetail, name='invitacion-detail'),
	url(r'^invitacionesNuevas/$', views.nuevaInvitacion, name='nuevaInvitacion'),
	url(r'^invitaciones/(?P<invit>\d+)/$', views.borrarInvitacion, name='deleteinvitacion'),
	url(r'^invitaciones/(?P<inviTa>\d+)/$', views.borrarInvitacionespitosas, name='deleteInvitaciones'),
	url(r'^organismos/$',views.organismos, name = 'organismos'),
	url(r'^organismos/(?P<Org>\d+)/$',views.borrarOrganismo, name='deleteOrganismo'),
	url(r'^organismosNuevos/$', views.nuevoOrganismo, name='nuevoOrganismo'),
	url(r'^personas/$', views.persona, name = 'pers'),
	url(r'^personas/(?P<perdet>\d+)/detail/$', views.personaDetalle, name='personaDetalle'),
	url(r'^sendEmail/$', views.sendEmail, name='sendEmail'),
	url(r'^mostrarPersonas/$', views.mostrarPersona, name='mostrarPersonas'),
	url(r'^mostrarPersonas/(?P<bPer>\d+)/$', views.borrarPersona, name='deletePersonas'),
	url(r'^nuevaPersona/$', views.nuevaPersona, name='newpers'),
	url(r'^actospersonas/(?P<idA>\d+)/detail/$', views.prueba, name='actospersonas'),
	url(r'^ubicacion/(?P<ubI>\d+)/detail/$', views.ubi, name='ubicacion'),
	#url(r'^ubicacion3/(?P<ubI>\d+)/(?P<idS>.+)/detail/$', views.ubi3, name='ubicacion3'),
	url(r'^ubicacion2/(?P<ubI>\d+)/(?P<idS>\d+)/detail/$', views.ubi2, name='ubicacion2'),
	url(r'^ubicacion/generarOrden/(?P<acto_id>\d+)/$', views.generarOrden, name='generarOrden'),
	url(r'^nuevoactoPersona/$', views.nuevoActoPersona, name='nuevoactoPersona'),
	url(r'^nuevoOrdena/$', views.nuevoOrden, name='nuevoOrdena'),
	url(r'^nuevoRol/$',views.nuevoRol, name='nuevoRol'),
	url(r'^invPers/(?P<act>\d+)/detail/$', views.invPers, name='invPers'),
	url(r'^incluir/$', views.incluir, name='incluir'),
	url(r'^persOrg/(?P<act>\d+)/(?P<org>\d+)/detail/$', views.personActo, name='personActo'),
	url(r'^nuevosAsientos/$', views.AsientoNuevo, name='asientosNuevos'),
	url(r'^404/$', django.views.defaults.page_not_found, ),
	url(r'^asientos/(?P<sal>\d+)/$', views.verAsientos, name='verAsientos'),
	url(r'^editaAsiento/(?P<idas>.+)/$',views.editAsiento,name='editAsientos'),
	url(r'^borrarAsiento/(?P<bAs>.+)/$',views.borrarAsiento,name='borrarAsientos'),
	
	] 

if settings.DEBUG is True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	

		
	
	#+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
