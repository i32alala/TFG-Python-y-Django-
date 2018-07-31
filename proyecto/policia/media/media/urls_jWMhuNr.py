from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proyecto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^policia/',include('policia.urls'), name ='policia'),
    url(r'^$',RedirectView.as_view(url='/policia/', permanent=True)),
   
    
) + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
