"""ibedc_cms_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include("authentication.urls")),
    path('api/v1/',include("dashboard.urls")),
    path('api/v1/',include("cmsadmin.urls")),
    path('api/v1/',include("customer.urls")),
    path('api/v1/',include("location.urls")),
    path('api/v1/',include("billing.urls")),
    path('api/v1/',include("payments.urls")),
    path('api/v1/',include("metering.urls")),
    path('api/v1/',include("gisassets.urls")),
    path('api/v1/',include("configurations.urls")),
    path('api/v1/',include("crmd.urls")),
    path('api/v1/',include("accountsmanager.urls")),
    path('api/v1/',include("caad.urls")),
    path('api/v1/',include("mails.urls")),
]
