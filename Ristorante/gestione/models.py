from django.db import models
from django.contrib.auth.models import User, Group
from ordini.models import Ordine

# Create your models here.

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, null=True, blank=True)
    cognome = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    immagine = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}"

class Valutazione(models.Model):
    ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE, null=True)
    valore = models.PositiveIntegerField()

    def __str__(self):
        return f"Valutazione ordine {self.ordine.id}"