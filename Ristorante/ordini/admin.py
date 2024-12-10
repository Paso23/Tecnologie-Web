from django.contrib import admin
from .models import Prodotto, Ordine

# Register your models here.

admin.site.register(Prodotto)
admin.site.register(Ordine)