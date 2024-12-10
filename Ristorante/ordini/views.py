from django.shortcuts import render, redirect
from .models import *
from gestione.models import Cliente
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from Ristorante.decorators import allowed_users
from django.contrib import messages

# Create your views here.

#funzione che gestisce il menu, passando al template 'carrello.html' la lista di prodotti su cui iterare e el quantità e tempistiche
def menu(request):

    ordine_categoria = ['antipasti', 'primi', 'secondi', 'dolci', 'bevande']

    def ordine_categoria_idx(categoria):
        return ordine_categoria.index(categoria)
    
    prod = Prodotto.objects.all()

    prodotti_ordinati = sorted(prod, key=lambda x: ordine_categoria_idx(x.categoria))
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.info(request,"effettua il login per ordinare.")
            return redirect('login')
        else:
            cliente = Cliente.objects.get(user=request.user)

            ordine_esistente = Ordine.objects.filter(cliente=cliente, status='nel carrello').first()
            if ordine_esistente:
                ordine_esistente.status = 'in preparazione'
                ordine_esistente.save()

            ordine, created = Ordine.objects.get_or_create(
                cliente=cliente, 
                status='nel carrello'
            )

            prodotti_aggiunti = False

            for prodotto in prodotti_ordinati:
                quantita = request.POST.get(f"quantita_{prodotto.id}", 0)
                
                if quantita and int(quantita) > 0:
                   
                    ordine_prodotto = ordineProdotto.objects.create(
                        ordine=ordine,
                        prodotto=prodotto,
                        quantita=int(quantita),
                        prezzo_unitario=prodotto.prezzo 
                    )
                    prodotti_aggiunti = True
            
            if not prodotti_aggiunti:
                messages.error(request, "Non hai aggiunto prodotti all'ordine")
                ordine.delete()
                return redirect('menu')
            
            tempo_prodotti = sum([5 * ordine_prodotto.quantita for ordine_prodotto in ordine.ordineprodotto_set.all()])
            ordini_in_preparazione = Ordine.objects.filter(status='in preparazione').count()
            tempo_ordini_in_preparazione = ordini_in_preparazione * 10

            tempo_totale = tempo_prodotti + tempo_ordini_in_preparazione
            ordine.tempo = tempo_totale
            ordine.save()

            return redirect('carrello') 
    
    ctx = {'prodotti': prodotti_ordinati}
    return render(request, "menu.html", context=ctx)


#funzione che seleziona l'ordine appena eseguito e stampa un recap di quest'ultimo
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def carrello(request):
    if request.user.is_authenticated:
        cliente = Cliente.objects.get(user=request.user)
        ordine = Ordine.objects.filter(cliente=cliente, status='nel carrello').first()

        if ordine:
            prodotti_ordinati = ordineProdotto.objects.filter(ordine=ordine)
        else:
            prodotti_ordinati = []

        totale = 0
        prodotti_con_totale = []

        for prodotto in prodotti_ordinati:
            totale_per_prod = prodotto.quantita * prodotto.prezzo_unitario
            prodotti_con_totale.append({
                'prodotto': prodotto,
                'totale': totale_per_prod
            })
            totale += totale_per_prod 

        return render(request, 'carrello.html', {
            'ordine': ordine,
            'prodotti_con_totale': prodotti_con_totale,
            'totale': totale
        })
    else:
        return redirect('/')

#funzione che permette di confermare l'ordine nel carrello
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def concludi_ordine(request):
    if request.user.is_authenticated:
        
        cliente = Cliente.objects.get(user=request.user)

        ordine = Ordine.objects.filter(cliente=cliente, status='nel carrello').first()

        if ordine:
            messages.success(request, "Ordine completato con successo.")
            ordine.status = 'in preparazione'
            ordine.save()

        return redirect('/') 

    return redirect('login') 

#funzione che permetted  di riproporre un ordine in quelli presenti
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def riproponi_ordine(request, ordine_id):
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        return redirect('home')
    
    ordine = get_object_or_404(Ordine, id=ordine_id, cliente=cliente)
        
    nuovo_ordine = Ordine.objects.create(cliente=cliente, data=timezone.now(), status='nel carrello', tempo = ordine.tempo + 10)  # Usa la data corrente
    
    prodotti = ordineProdotto.objects.filter(ordine=ordine)

    for prodotto in prodotti:
        ordineProdotto.objects.create(ordine=nuovo_ordine, prodotto=prodotto.prodotto, quantita=prodotto.quantita,  prezzo_unitario=prodotto.prezzo_unitario)

    return redirect('carrello')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def rimuovi_ordine(request, ordine_id):
    try:
        cliente = Cliente.objects.get(user=request.user)
    except Cliente.DoesNotExist:
        return redirect('home')
    
    ordine = get_object_or_404(Ordine, id=ordine_id, cliente=cliente)
    ordine.delete()
    messages.success(request, "Ordine eliminato con successo.")
    return redirect('/')

#funzione che, all'interno del carrello, permette l'annullamento dell'ordine corrente
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def annulla_ordine(request):
    if request.user.is_authenticated:
        cliente = Cliente.objects.get(user = request.user)
        ordine = get_object_or_404(Ordine, cliente = cliente, status = 'nel carrello')
        ordine.delete()
    
    return redirect('menu')