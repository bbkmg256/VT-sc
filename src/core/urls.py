"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.conf import settings

# MODO DEBUG
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Inicio
    path("", views.home_view),
    path("home/", views.home_view, name="home_view"),
    path("tablones/", include("src.apps.tablon.urls")),
]

# TODA ESTA MIERDA NO SE LEE CUANDO SE HACE EL PROXY INVERSO EN NGiNX
# URLs solo para modo DEBUG (IMPORTANTE PARA PRUEBAS CON GUNICORN)
if settings.DEBUG:
    # Agrega las rutas del contenido multimedia
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Cuando se NO se usa el modulo settings original
    if not settings.SETTINGS_DEFAULT:
        # Agrega las rutas de los archivos estáticos
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
