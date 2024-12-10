from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from ristoratore.models import Richiesta


class FormCreazioneUtente(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2'] 

class AggiungiRichiesta(forms.ModelForm):
    
    class Meta:
        model = Richiesta
        fields = ['descrizione']
