from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.loginPage, name="login"),
    path('logout', views.logoutPage, name="logout"),
    path('registrazione', views.registrazionePage, name="registrazione"),
    path('controllo_valutazione/<int:ordine_id>/', views.controllo_valutazione, name="controllo_valutazione"),
    path('crea_valutazione/<int:ordine_id>/', views.crea_valutazione, name="crea_valutazione"),
    path('gestione_richieste', views.gestione_richieste_cliente, name="gestione_richieste"),
    path('rimuovi_richiesta/<int:richiesta_id>/', views.rimuovi_richiesta, name="rimuovi_richiesta"),
    path('aggiungi_richiesta/<int:annuncio_id>/', views.aggiungi_richiesta, name="aggiungi_richiesta"),
]
