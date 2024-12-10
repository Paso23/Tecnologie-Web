from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.menu, name="menu"),
    path('carrello/', views.carrello, name='carrello'),
    path('concludi_ordine/', views.concludi_ordine, name='concludi_ordine'),
    path('riproponi_ordine/<int:ordine_id>/', views.riproponi_ordine, name='riproponi_ordine'),
    path('rimuovi_ordine/<int:ordine_id>/', views.rimuovi_ordine, name='rimuovi_ordine'),
    path('annulla_ordine', views.annulla_ordine, name='annulla_ordine'),
    #path('gestioneMenu', views.aggiungi_prodotto, name='aggiungi_prodotto')
]