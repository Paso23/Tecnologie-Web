from django.test import TestCase
##from ordini.models import *
from ristoratore.forms import AggiungiProdotto

# Create your tests here.

class TestRistoratore(TestCase):

    #test che controlla la validità del form provando l'inserimento di un prezzo negativo
    def testCreaProdottoPrezzo(self):
        prezzo = -10
        form = AggiungiProdotto(prezzo)
        self.assertNotEqual(form.is_valid, True)
    
    #test che controlla la validità del form provando l'inserimento di una categoria giusta
    def testCreaProdottoCategoria(self):
        categoria = "antipasti"
        form = AggiungiProdotto(categoria)
        self.assertNotEqual(form.is_valid, False)