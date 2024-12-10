from django.test import TestCase
from .models import *
from gestione.models import *

class TestOrdini(TestCase):

    def setUp(self):
        user = User.objects.create(username="prova", password="pppp1111")
        cliente = Cliente.objects.create(user = user)
        ordine = Ordine.objects.create(cliente=cliente)

    #test che verifica se l'ordine è stato effettuato dal cliente
    def testOrdineDelCliente(self):
        cliente = Cliente.objects.get(user__username="prova")
        ordine = Ordine.objects.get(cliente=cliente)
        self.assertEqual(ordine.cliente, cliente)
        self.assertEqual(ordine.cliente.user.username, "prova")