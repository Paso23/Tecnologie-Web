from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Prodotto(models.Model):
    CATEGORIA = (
        ('antipasti','antipasti'),
        ('primi','primi'),
        ('secondi','secondi'),
        ('dolci','dolci'),
        ('bevande','bevande')
    )

    nome = models.CharField(max_length=50)
    categoria = models.CharField(max_length=20,choices=CATEGORIA)
    descrizione = models.CharField(max_length=200, null=True, blank=True, default="-")
    prezzo = models.DecimalField(max_digits=6, decimal_places=2, validators=[MaxValueValidator(100), MinValueValidator(1)])

    def __str__(self):
        return self.nome

class Ordine(models.Model):
    STATUS = (
        ('in preparazione','in preparazione'),
        ('pronto','pronto'),
        ('nel carrello','nel carrello'),
    )
    cliente = models.ForeignKey('gestione.Cliente', null=True, on_delete=models.CASCADE)
    #prodotto = models.ForeignKey(prodotti, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, null=True, choices=STATUS, default="nel carrello")
    data = models.DateTimeField(auto_now_add=True, null=True)
    tempo = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)

class ordineProdotto(models.Model):
    ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE)
    prodotto = models.ForeignKey(Prodotto, on_delete=models.CASCADE)
    quantita = models.PositiveIntegerField()
    prezzo_unitario = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.prodotto.nome} - {self.quantita} x {self.prezzo_unitario}€"