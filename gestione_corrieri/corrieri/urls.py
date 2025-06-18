from django.urls import path, include
from . import views
from . import api_views
from corrieri.views import visualizza_consegne




urlpatterns = [
    # ... altre url ...
    path('lista_ordini/', views.ordini, name='lista_ordini'),
    path('assegna_ordini/', views.assegna_ordini_view, name='assegna_ordini'),
    path('crea_ordine/', views.crea_ordine, name='crea_ordine'),
    path('elimina_ordine/<int:id_ordine>/', views.elimina_ordine, name='elimina_ordine'),
    path('dettagli_consegna/<int:id_consegna>/', views.dettagli_consegna, name='dettagli_consegna'),
    path('dettaglio_ordine/<int:id_ordine>/', views.dettaglio_ordine, name='dettaglio_ordine'),
    path('modifica_ordine/<int:id_ordine>/', views.modifica_ordine, name='modifica_ordine'),
    path('api/ordini/<int:id_ordine>/', views.api_dettaglio_ordine, name='api_dettaglio_ordine'),
    path('lista_corrieri/', views.lista_corrieri, name='lista_corrieri'),
    path('crea_corriere/', views.crea_corriere, name='crea_corriere'),
    path('dettaglio_corriere/<int:id_corriere>/', views.dettaglio_corriere, name='dettaglio_corriere'),
    path('modifica_corriere/<int:id_corriere>/', views.modifica_corriere, name='modifica_corriere'),
    path('elimina_corriere/<int:id_corriere>/', views.elimina_corriere, name='elimina_corriere'),  
    path('lista_mezzi/', views.lista_mezzi, name='lista_mezzi'),
    path('crea_mezzo/', views.crea_mezzo, name='crea_mezzo'),
    path('modifica_mezzo/<int:id_veicolo>/', views.modifica_mezzo, name='modifica_mezzo'),
    path('dettaglio_mezzo/<int:id_veicolo>/', views.dettaglio_mezzo, name='dettaglio_mezzo'),
    path('elimina_mezzo/<int:id_veicolo>/', views.elimina_mezzo, name='elimina_mezzo'),
    # API Endpoints
    path('api/ordini/', api_views.registra_ordine, name='api_registra_ordine'),
    path('api/ordini/<str:codice_assegnazione>/', api_views.stato_ordine, name='api_stato_ordine'),
    path('api/corrieri/<str:codice_corriere>/consegne/', api_views.consegne_corriere, name='api_consegne_corriere'),
    path('api-test/', views.api_test, name='api_test'),
    path('consegne/', visualizza_consegne, name='visualizza_consegne')
]