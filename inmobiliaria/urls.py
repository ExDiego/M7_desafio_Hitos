"""
URL configuration for inmobiliaria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('propiedad/<int:id>/', detalle_propiedad , name='detalle'),
    path('propiedades/<int:id>/generar-solicitud/', generar_solicitud_arriendo, name='generar_solicitud_arriendo'),
    path('propiedad/<int:id>/editar_propiedad',actualizar_propiedad, name='editar_propiedad'),
    path('propiedad/<int:id>/eliminar_propiedad',eliminar_propiedad, name='eliminar_propiedad'),
    path('alta-propiedad/', crear_propiedad, name='alta_propiedad'),
    path('solicitudes/', solicitudes_arrendador, name='solicitudes_arrendador'),
    path('dashboard/', dashboard, name='dashboard'),
    path('perfil/', actualizar_usuario, name='actualizar_usuario'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)