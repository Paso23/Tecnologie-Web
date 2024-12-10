from django.test import TestCase
from http import HTTPStatus
from django.urls import reverse
from .models import *

# Create your tests here.

class TestHomepage(TestCase):

    def setUp(self):
        Group.objects.create(name = "Customers")
        Group.objects.create(name = "Ristoratori")
        gruppoClienti = Group.objects.get(name = "Customers")
        gruppoRistoratori = Group.objects.get(name = "Ristoratori")
        utenteCliente = User.objects.create_user(username= "prova", password="qqqq1111")
        utenteRistoratore = User.objects.create_user(username= "prova2", password="wwww1111", is_staff = True)

        utenteCliente.groups.add(gruppoClienti)
        utenteRistoratore.groups.add(gruppoRistoratori)

    #test che verifica se è presente la stringa "Ordini Conclusi:" all'interno della pagina homepage del cliente
    def testVistaClienteHomepage(self):
        self.client.login(username = "prova", password = "qqqq1111")
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Ordini Conclusi:")
    
    #test che verifica se è presente la stringa "Gestione ordini" all'interno della pagina homepage del ristoratore
    def testVistaRistoratoreHomepage(self):
        self.client.login(username = "prova2", password = "wwww1111")
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Gestione ordini")
