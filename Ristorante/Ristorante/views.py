from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from gestione.models import *
from ordini.models import *
from .forms import ImpostazioniForm
from django.contrib.auth.decorators import login_required
from Ristorante.decorators import allowed_users
from django.contrib import messages

#funzione che gestisce l'homepage della web-app, mostrando gli ordini dei clienti e la media delle valutazioni
def homepage(request):
    ordini_con_username = []
    valutazioni = Valutazione.objects.all()
    if valutazioni.exists():
        media = sum([valutazione.valore for valutazione in valutazioni]) / valutazioni.count()
    else:
        media = 0
    if request.user.is_authenticated:
        if request.user.is_staff:
            ordini = Ordine.objects.filter(status='in preparazione').order_by('data')
            
            for ordine in ordini:
                prodotti = ordineProdotto.objects.filter(ordine=ordine)
                username = ordine.cliente.user.username
                ordini_con_username.append({
                    'ordine': ordine,
                    'prodotti': prodotti,
                    'username': username
                })
            return render(request, 'home.html', context={'ordini_con_username':ordini_con_username, 'media':media})
        else:
            try:   
                cliente = Cliente.objects.get(user=request.user)
            except Cliente.DoesNotExist:
                return render(request, 'home.html', context={'error': 'Cliente non trovato'})
            
            ultimi_ordini = Ordine.objects.filter(cliente=cliente, status='in preparazione').order_by('-data')[:5]
            ordini_conclusi = Ordine.objects.filter(cliente=cliente, status='pronto')

            for ordine_in_preparazione in ultimi_ordini:
                ordine_in_preparazione.prodotti = ordineProdotto.objects.filter(ordine=ordine_in_preparazione)
            for ordine_concluso in ordini_conclusi:
                ordine_concluso.prodotti = ordineProdotto.objects.filter(ordine=ordine_concluso)

            ctx = {'ultimi_ordini': ultimi_ordini, 'ordini_conclusi': ordini_conclusi, 'media': media}
            return render(request, 'home.html', context=ctx)
    else:
        templ = "home.html"
        ctx = {'media':media}
        return render(request, template_name = templ, context=ctx)


#funzione che permette la modifica tramite form delle informazioni del clinte corrente
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def gestioneUtente(request):
    try:
            cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
            raise Http404("Cliente non trovato.")
        
    if request.method == 'POST':
        form = ImpostazioniForm(request.POST, request.FILES, instance=cliente)

        if form.is_valid():
            form.save()
            messages.success(request, "Informazioni aggiornate con successo.")
            return redirect('impostazioni')
        else:
            messages.error(request,"Uno dei campi non è valido: caratteri per nome e cognome, numeri per telefono.")
            return redirect('impostazioni')
    else:
        form = ImpostazioniForm(instance=cliente)

    ctx = {'form': form}

    templ = "impostazioni.html"
    return render(request, template_name=templ, context=ctx)
