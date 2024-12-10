from django.db import models
from gestione.models import Cliente

# Create your models here.

#annunci creati dal ristoratore che vengono visionati dai clienti
class Annuncio(models.Model):
    tipologia = models.CharField(max_length=50, null=True)
    descrizione = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.tipologia
    

#richieste fatte dagli utenti relative ad un annuncio
class Richiesta(models.Model):
    STATUS = (
        ('in attesa','in attesa'),
        ('approvata','approvata'),
        ('rifiutata','rifiutata'),
    )
    status = models.CharField (max_length=20, null=True, choices=STATUS, default="in attesa")
    annuncio = models.ForeignKey(Annuncio, null=True, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, null=True, on_delete=models.CASCADE)
    descrizione = models.CharField(max_length=200, null=True)
    motivazione = models.CharField(max_length=200, blank=True, null=True)
