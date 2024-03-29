"""dj110 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login

admin.site.site_header = "CiTeSoft"
admin.site.site_title = "CITESOFT"
admin.site.index_title = "Super_Administrador"


admin.autodiscover()
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Inventario.urls')),
    url(r'^$', login, {'template_name' : 'Registro/login.html', 'redirect_authenticated_user' : True}, name = 'login'),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
