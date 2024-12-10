from django.forms import ModelForm
from ordini.models import Prodotto
from django import forms
from .models import Annuncio, Richiesta

class AggiungiProdotto(ModelForm):
    class Meta:
        model = Prodotto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['descrizione'].initial = '-'
    
    def clean_prezzo(self):
        prezzo = self.cleaned_data.get('prezzo')
        if prezzo < 0 :
            raise forms.ValidationError("Il prezzo non può essere negativo.")
        return prezzo
    
    def clean_descrizione(self):
        descrizione = self.cleaned_data.get('descrizione', '')
        return descrizione if descrizione else '-'

class AggiungiAnnuncio(ModelForm):
    class Meta:
        model = Annuncio
        fields = '__all__'

class InserisciMotivazione(ModelForm):
    class Meta:
        model = Richiesta
        fields = ['motivazione']