"""
URL configuration for gestione_corrieri project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from corrieri import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('corrieri.urls')),
    path('interfaccia_admin/', views.interfaccia_admin, name='admin'),
    path('home/', views.home, name='home'),
    path('lista_ordini/', views.ordini, name='lista_ordini'),
    path('assegna_ordini/', views.assegna_ordini_view, name='assegna_ordini'),
    path('crea_ordine/', views.crea_ordine, name='crea_ordine'),
    path('elimina_ordine/<int:id_ordine>/', views.elimina_ordine, name='elimina_ordine'),
    path('lista_consegne/', views.lista_consegne, name='lista_consegne'),
    path('dettagli_consegna/<int:id_consegna>/', views.dettagli_consegna, name='dettagli_consegna'),
    path('dettaglio_ordine/<int:id_ordine>/', views.dettaglio_ordine, name='dettaglio_ordine'),
    path('modifica_ordine/<int:id_ordine>/', views.modifica_ordine, name='modifica_ordine'),
    path('api/ordini/<int:id_ordine>/', views.api_dettaglio_ordine, name='api_dettaglio_ordine'),
    path('lista_corrieri/', views.lista_corrieri, name='lista_corrieri'),
    path('crea_corriere/', views.crea_corriere, name='crea_corriere'),
    path('dettaglio_corriere/<int:id_corriere>/', views.dettaglio_corriere, name='dettaglio_corriere'),
    path('modifica_corriere/<int:id_corriere>/', views.modifica_corriere, name='modifica_corriere'),
    path('elimina_corriere/<int:id_corriere>/', views.elimina_corriere, name='elimina_corriere'),
    # include('co')
]
