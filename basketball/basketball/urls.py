"""
URL configuration for basketball project.

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
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path("accounts/", include('allauth.urls')),
    path("calendar/",include("calendar_basket.urls")),
    path("clasificacion/",include("clasificacion.urls")),
    path("statistics/",include("statistics_basketball.urls")),
    path("perfil/",include("perfil.urls")),
    path('api/v1/api-auth/', include('rest_framework.urls', namespace='rest_framework'), name='api-auth'),
    path('api/v1/', include('calendar_basket.api.v1.urls')),
    path('api/v1/', include('clasificacion.api.v1.urls')),
    path('api/v1/', include('statistics_basketball.api.v1.urls')),
    path('api/v1/', include('perfil.api.v1.urls')),
]
