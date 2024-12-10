from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_ristoratore, name="menu_ristoratore"),
    path('add_prodotto/', views.aggiungi_prodotto, name="aggiungi_prodotto"),
    path('elimina_prodotto/<int:p_id>/', views.elimina_prodotto, name="elimina_prodotto"),
    path('concludi_ordine/<int:ordine_id>/', views.concludi_ordine, name="concludi_ordine"),
    path('gestione_annunci', views.gestione_annunci, name="gestione_annunci"),
    path('elimina_annuncio/<int:annuncio_id>/', views.elimina_annuncio, name="elimina_annuncio"),
    path('crea_annuncio', views.crea_annuncio, name="crea_annuncio"),
    path('gestione_richieste/<int:richiesta_id>', views.gestione_richieste, name="gestione_richieste"),
    path('inserisci_motivazione/<int:richiesta_id>/', views.inserisci_motivazione, name='inserisci_motivazione'),
    #path('gestioneMenu', views.aggiungi_prodotto, name='aggiungi_prodotto')
]