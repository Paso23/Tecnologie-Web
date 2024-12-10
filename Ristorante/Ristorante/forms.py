from django import forms
from gestione.models import Cliente
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ImpostazioniForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cognome', 'telefono', 'immagine']
    
    nome = forms.CharField(required=False)
    cognome = forms.CharField(required=False)
    telefono = forms.CharField(required=False)  # Campo non obbligatorio
    immagine = forms.ImageField(required=False) 

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not telefono.isdigit():
            raise ValidationError(_('Il telefono deve contenere solo numeri.'))
        return telefono
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome and not nome.isalpha():
            raise ValidationError(_('Il nome deve contenere solo lettere.'))
        return nome

    def clean_cognome(self):
        cognome = self.cleaned_data.get('cognome')
        if cognome and not cognome.isalpha():
            raise ValidationError(_('Il cognome deve contenere solo lettere.'))
        return cognome