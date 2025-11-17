"""
URL configuration for API_albuna project.

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
from django.http import JsonResponse # <-- IMPORT BARU

# Fungsi Healthcheck: Hanya mengembalikan status 'ok'
def health_check(request):
    """Fungsi ini digunakan oleh Railway untuk memverifikasi server berjalan."""
    return JsonResponse({'status': 'ok'}, status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('api/', include('product_catalog.urls')),
]