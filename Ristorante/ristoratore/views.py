from django.shortcuts import render, redirect, get_object_or_404
from .forms import AggiungiProdotto, AggiungiAnnuncio, InserisciMotivazione
from ordini.models import *
from .models import Annuncio, Richiesta
from gestione.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Ristorante.decorators import allowed_users

# Create your views here.

#funzione che gestisce il menu lato ristoratore, mostrando i vari prodotti e dando la possibilità all'utente staff di inserire ed eliminare i vari prodotti
@login_required(login_url='login')
@allowed_users(allowed_roles=['Ristoratori'])
def menu_ristoratore(request):

    ordine_categoria = ['antipasti', 'primi', 'secondi', 'dolci', 'bevande']

    def ordine_categoria_idx(categoria):
        return ordine_categoria.index(categoria)
    
    prod = Prodotto.objects.all()

    prodotti_ordinati = sorted(prod, key=lambda x: ordine_categoria_idx(x.categoria))

    ctx = {'prodotti': prodotti_ordinati}
    return render(request, "menu.html", context=ctx)

#funzione che, dato in ingresso l'id del prodotto selezionato, permette la sua eliminazione dal menu
@login_required(login_url='login')
@allowed_users(allowed_roles=['Ristoratori'])
def elimina_prodotto(request, p_id):
    
    if request.method == "POST":
        prodotto = get_object_or_404(Prodotto, id=p_id)
        prodotto.delete()
        messages.success(request, "Prodotto "+ prodotto.nome +" eliminato con successo.")
        return redirect('menu_ristoratore')
    
    return redirect('menu_ristoratore')

#funzione che permette all'utente staff di aggiungere un nuovo prodotto al menu tramite l'uso del form AggiungiProdotto
@login_required(login_url='login')
@allowed_users(allowed_roles=['Ristoratori'])
def aggiungi_prodotto(request):

    if request.method == 'POST':
        form = AggiungiProdotto(request.POST)

        if form.is_valid():  
            nuovo_prod = form.save()
            nome = nuovo_prod.nome
            messages.success(request, f'Voce "{nome}" inserita nel menù')
            return redirect('menu_ristoratore')
        
        messages.error(request,"Inserisci valori coerenti")
    else:
        form = AggiungiProdotto()
        messages.error(request,"Prezzo non valido")

    ctx = {'form': form}
    return render(request, "add_prodotto.html", context=ctx)

#funzione che, prendendo in ingresso l'id dell'ordine, permette di conclude l'ordine di un determinato cliente, settando il suo status a 'pronto'
@login_required(login_url='login')
@allowed_users(allowed_roles=['Ristoratori'])
def concludi_ordine(request, ordine_id):
    if request.method == 'POST':
        ordine = Ordine.objects.get(id = ordine_id)
        ordine.status = 'pronto'
        ordine.save()
        messages.success(request, f'Confermata la preparazione dell Ordine {ordine_id}')
        return redirect('/')
    else:
        messages.error(request, 'Errore nella conferma dell Ordine')
        return redirect('/')

#funzione che permette di visualizzare tutti gli annunci presenti
@login_required(login_url='login')
@allowed_users(allowed_roles=['Ristoratori'])
def gestione_annunci(request):
    richieste_con_username = []
    annunci = Annuncio.objects.all()
    richieste = Richiesta.objects.filter(status='in attesa')
    if annunci.exists():
        if richieste.exists():
            for richiesta in richieste:
                username = richiesta.cliente.user.username
                tipologia = richiesta.annuncio.tipologia
                richieste_con_username.append({
                    'richiesta': richiesta,
                    'username': username,
                    'tipologia':tipologia
                })
            return render(request, 'gestione_annunci.html', context={'richieste_con_username':richieste_con_username, 'annunci':annunci})
        else:
            ctx= {'annunci':annunci}
            messages.info(request,'Al momento non sono presenti richieste lavorative')
            return render(request, "gestione_annunci.html", context=ctx)
    else:
        messages.info(request, "Al momento non sono presenti annunci.")
    
    return render(request,'gestione_annunci.html')

#funzione che, preso in ingresso l'id di un annuncio, permette di eliminarlo
@login_required(login_url='login')
@allowed_users(allowed_roles=['Ristoratori'])
def elimina_annuncio(request,annuncio_id):
    
    if request.method == "POST":
        annuncio = get_object_or_404(Annuncio, id=annuncio_id)
        annuncio.delete()
        messages.success(request,'annuncio eliminato con successo')
        return redirect('gestione_annunci')
    
    return redirect('gestione_annunci')

#funzione che permette di creare un nuovo annuncio tramite l'utilizzo del form AggiungiAnnuncio
@login_required(login_url='login')
@allowed_users(allowed_roles=['Ristoratori'])
def crea_annuncio(request):
    form = AggiungiAnnuncio()
    if request.method == 'POST':
        form = AggiungiAnnuncio(request.POST)
        if form.is_valid():
            nuovo_annuncio = form.save()
            nome = nuovo_annuncio.tipologia
            messages.success(request, f'Annuncio per "{nome}" inserito.')
            return redirect('gestione_annunci')
    
    ctx = {'form':form}
    return render(request, "crea_annuncio.html", context=ctx)

#funzione che, preso in ingresso l'ID della richiesta, permette di scartarla o accettarla
@login_required(login_url='login')
@allowed_users(allowed_roles=['Ristoratori'])
def gestione_richieste(request, richiesta_id):
    richiesta = get_object_or_404(Richiesta, id=richiesta_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'Scarta':
            richiesta.status = 'rifiutata'
            richiesta.save()
            return redirect('inserisci_motivazione', richiesta_id = richiesta_id)
        elif action =='Accetta':
            richiesta.status = 'accettata'
            richiesta.motivazione = 'La invitiamo a contattarci per ulteriori informazioni!'
            richiesta.save()
            messages.success(request, "Risposta avvenuta con successo.")
    
    return redirect('gestione_annunci')

#funzione che, preso in ingresso l'ID di una richiesta scartata, permette di inserire una motivazione per il rifiuto
@login_required(login_url='login')
@allowed_users(allowed_roles=['Ristoratori'])
def inserisci_motivazione(request, richiesta_id):
    richiesta = get_object_or_404(Richiesta, id=richiesta_id)
    form = InserisciMotivazione(instance=richiesta)
    if request.method == 'POST':
        form = InserisciMotivazione(request.POST, instance=richiesta)
        if form.is_valid():
            richiesta.motivazione = form.cleaned_data['motivazione']
            richiesta.save()
            messages.success(request, "La richiesta è stata rifiutata con successo.")
            return redirect('gestione_annunci')
    return render(request, 'inserisci_motivazione.html', {'form': form, 'richiesta': richiesta})