from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from .models import *
from ristoratore.models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import AggiungiRichiesta
from Ristorante.decorators import *

# Create your views here.

#funzione che gestisce la pagina di login
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'username o password non corretti')

        ctx = {}
        return render(request, 'login.html', context=ctx)

#funzione che gestisce la pagina di registrazione, aggiungendo l'utente appena registrato al gruppo Customers
def registrazionePage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserCreationForm

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account creato per '+ username)

                group = Group.objects.get(name='Customers')
                user.groups.add(group)
                cliente = Cliente.objects.create(
                    user=user,
                    nome="",
                    cognome="",  
                    telefono=""  
                )

                return redirect('login')

        ctx = {'form': form}

        return render(request, 'registration.html', context=ctx)

#funzione che permette il logout dell'utente corrente tramite la funzione logout bult-in di Django
def logoutPage(request):
    logout(request)
    return redirect('login')

#funzione che controlla se è già stata effettuata una valutazione di un determinato ordine
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def controllo_valutazione(request, ordine_id):
    if request.method == 'POST':
        try:
            val = Valutazione.objects.get(ordine=ordine_id)
        except ObjectDoesNotExist:
            val = None 
        if val != None:
            messages.error(request, "Hai già effettuato una valutazione per questo ordine.")
            return redirect('/')
        
    ctx = {"ordine_id": ordine_id}
    return render(request, "effettua_valutazione.html", context=ctx)

#funzione che permette di effettuare una valutazione su un determinato ordine
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def crea_valutazione(request, ordine_id):
    if request.method  == 'POST':
        val = request.POST.get('rate')
        ordine_id = request.POST.get('ordine_id')
        if val:
            ordine = Ordine.objects.get(id=ordine_id)
            valutazione = Valutazione.objects.create(ordine = ordine, valore=val)
            messages.success(request, "Grazie per il tuo feedback!")
            return redirect('/')

#funzione che permette la visualizzazione e gestione delle richieste lavorative inoltrate dal cliente
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def gestione_richieste_cliente(request):
    richieste_con_tipologia = []
    cliente = Cliente.objects.get(user=request.user)
    nome = cliente.nome
    richieste = Richiesta.objects.filter(cliente_id = cliente.id)
    annunci = Annuncio.objects.all()
    if annunci.exists:
        if richieste.exists:
            for richiesta in richieste:
                tipologia = richiesta.annuncio.tipologia
                motivazione = richiesta.motivazione
                richieste_con_tipologia.append({
                    'richiesta': richiesta,
                    'tipologia':tipologia,
                    'motivazione':motivazione
                })
            ctx = {'richieste_con_tipologia': richieste_con_tipologia, 'annunci': annunci}
            return render(request, "gestione_richieste.html", context=ctx)
        else:
            messages.info(request, "Non sono presenti richieste lavorative per " + nome)
            ctx = {'richieste': richieste, 'annunci': annunci}
            return render(request, "gestione_richieste.html", context=ctx)
    else:
        messages.info(request, "Al momento non sono presenti nuovi annuci.") 
        return redirect('/')

#funzione che permette all'utente di rimuovere una richiesta lavorativa
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def rimuovi_richiesta(request, richiesta_id):
    if request.method == "POST":
        richiesta = get_object_or_404(Richiesta, id=richiesta_id)
        richiesta.delete()
        messages.success(request,'Richiesta eliminata con successo')
        return redirect('gestione_richieste')
    
    return redirect('gestione_richieste')

#funzione che permetta all'utente di create una richiesta lavorativa per un determinato annuncio
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def aggiungi_richiesta(request, annuncio_id):
    cliente = Cliente.objects.get(user = request.user)
    annuncio = Annuncio.objects.get(id = annuncio_id)
    form = AggiungiRichiesta()
    if request.method == 'POST':
        form = AggiungiRichiesta(request.POST)
        if form.is_valid():
            nuova_richiesta = form.save(commit=False)
            nuova_richiesta.annuncio = annuncio
            nuova_richiesta.cliente = cliente
            nuova_richiesta.save()
            messages.success(request, "Richiesta inoltrata con successo")
            return redirect('gestione_richieste')
    ctx = {'form':form}
    return render(request, "add_richiesta.html", context=ctx)