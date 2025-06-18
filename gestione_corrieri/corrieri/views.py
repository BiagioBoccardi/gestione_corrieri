from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User  # importa il modello User
from corrieri.models import Ordine, Corriere, Consegna
# from corrieri.assegnazione import assegna_ordini
from corrieri.forms import OrdineForm  # Devi creare questo form
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers 
from django import forms
from .models import Veicolo
import json
from .models import NotificaConsegna
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("Ricevuto webhook:", data)
        return JsonResponse({"status": "Ordine ricevuto"}, status=200)
    return JsonResponse({"error": "Solo POST"}, status=405)

# Serializer for Ordine model
class OrdineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordine
        fields = '__all__'

class VeicoloForm(forms.ModelForm):
    class Meta:
        model = Veicolo
        fields = ['Codice_Corriere', 'capacità_massima', 'Targa_mezzo']

def home(request):
    ordini_assegnati = Ordine.objects.filter(stato="ASSEGNATO").count()
    ordini_transito = Ordine.objects.filter(stato="TRANSITO").count()
    ordini_in_consegna = Ordine.objects.filter(stato="IN_CONSEGNA").count()
    ordini_completati = Ordine.objects.filter(stato="COMPLETATO").count()
    corrieri = Corriere.objects.all()
    dati_percorso = []
    for corriere in corrieri:
        tappe = []
        # posizione attuale del corriere
        if corriere.latitudine and corriere.longitudine:
            tappe.append({
                'nome': f"Partenza: {corriere.nome}",
                'lat': corriere.latitudine,
                'lng': corriere.longitudine
            })
        # tappe degli ordini assegnati
        consegne = Consegna.objects.filter(id_corriere=corriere).select_related('id_ordine').order_by('id_ordine__data_e_ora_ordine')
        for c in consegne:
            ordine = c.id_ordine
            if ordine.latitudine and ordine.longitudine:
                tappe.append({
                    'nome': ordine.indirizzo,
                    'lat': ordine.latitudine,
                    'lng': ordine.longitudine
                })
        dati_percorso.append({'corriere': corriere.nome, 'tappe': tappe})
    return render(request, 'home.html', {
        'ordini_assegnati': ordini_assegnati,
        'ordini_transito': ordini_transito,
        'ordini_in_consegna': ordini_in_consegna,
        'ordini_completati': ordini_completati,
        'corrieri': corrieri,
        'dati_percorso_json': json.dumps(dati_percorso)
    })

def interfaccia_admin(request):
    return render(request, 'Interfaccia_admin.html')
def ordini(request):
    ordini = Ordine.objects.all().order_by('-data_e_ora_ordine')
    return render(request, 'lista_ordini.html', {'ordini': ordini})
def assegna_ordini_view(request):
    if request.method == "POST":
        # assegna_ordini()
        return redirect('lista_ordini')  # Assicurati che 'lista_ordini' sia il nome della tua lista ordini
def crea_ordine(request):
    if request.method == "POST":
        form = OrdineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ordini')
        else:
            print("Errore form non valido")
            #return render(request, 'crea_ordine.html', {'form': form})
    else:
        form = OrdineForm()
    return render(request, 'crea_ordine.html', {'form': form})
def elimina_ordine(request, id_ordine):
    ordine = Ordine.objects.get(id_ordine=id_ordine)
    ordine.delete()
    return redirect('lista_ordini')
def lista_consegne(request):
    consegne = Consegna.objects.select_related('id_ordine', 'id_corriere', 'id_veicolo').all()
    return render(request, 'lista_consegne.html', {'consegne': consegne})
def dettagli_consegna(request, id_consegna):
    consegna = Consegna.objects.select_related('id_ordine', 'id_corriere', 'id_veicolo').get(id_consegna=id_consegna)
    return render(request, 'dettagli_consegna.html', {'consegna': consegna})
def dettaglio_ordine(request, id_ordine):
    ordine = Ordine.objects.get(id_ordine=id_ordine)
    return render(request, 'dettaglio_ordine.html', {'ordine': ordine})
def modifica_ordine(request, id_ordine):
    ordine = Ordine.objects.get(id_ordine=id_ordine)
    if request.method == "POST":
        form = OrdineForm(request.POST, instance=ordine)
        if form.is_valid():
            form.save()
            return redirect('lista_ordini')
    else:
        form = OrdineForm(instance=ordine)
    return render(request, 'modifica_ordine.html', {'form': form, 'ordine': ordine})

@api_view(['GET'])
def api_dettaglio_ordine(request, id_ordine):
    try:
        ordine = Ordine.objects.get(id_ordine=id_ordine)
    except Ordine.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrdineSerializer(ordine)
    return Response(serializer.data)

def lista_corrieri(request):
    corrieri = Corriere.objects.all()
    return render(request, 'lista_corrieri.html', {'corrieri': corrieri})

class CorriereForm(forms.ModelForm):
    class Meta:
        model = Corriere
        fields = ['nome', 'capacità_massima', 'posizione_attuale']

def crea_corriere(request):
    if request.method == "POST":
        form = CorriereForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_corrieri')
    else:
        form = CorriereForm()
    return render(request, 'crea_corriere.html', {'form': form})

def dettaglio_corriere(request, id_corriere):
    corriere = get_object_or_404(Corriere, id_corriere=id_corriere)
    return render(request, 'dettaglio_corriere.html', {'corriere': corriere})
def modifica_corriere(request, id_corriere):
    corriere = get_object_or_404(Corriere, id_corriere=id_corriere)
    if request.method == "POST":
        form = CorriereForm(request.POST, instance=corriere)
        if form.is_valid():
            form.save()
            return redirect('lista_corrieri')
    else:
        form = CorriereForm(instance=corriere)
    return render(request, 'modifica_corriere.html', {'form': form, 'corriere': corriere})
def elimina_corriere(request, id_corriere):
    corriere = Corriere.objects.get(id_corriere=id_corriere)
    corriere.delete()
    return redirect('lista_corrieri')
def lista_mezzi(request):
    mezzi = Veicolo.objects.all()
    return render(request, 'lista_mezzi.html', {'mezzi': mezzi})
def crea_mezzo(request):
    if request.method == "POST":
        form = VeicoloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_mezzi')
    else:
        form = VeicoloForm()
    return render(request, 'crea_mezzo.html', {'form': form})

def modifica_mezzo(request, id_veicolo):
    mezzo = get_object_or_404(Veicolo, id_veicolo=id_veicolo)
    if request.method == "POST":
        form = VeicoloForm(request.POST, instance=mezzo)
        if form.is_valid():
            form.save()
            return redirect('lista_mezzi')
    else:
        form = VeicoloForm(instance=mezzo)
    return render(request, 'modifica_mezzo.html', {'form': form, 'mezzo': mezzo})
def dettaglio_mezzo(request, id_veicolo):
    mezzo = get_object_or_404(Veicolo, id_veicolo=id_veicolo)
    return render(request, 'dettaglio_mezzo.html', {'mezzo': mezzo})

def elimina_mezzo(request, id_veicolo):
    mezzo = get_object_or_404(Veicolo, id_veicolo=id_veicolo)
    mezzo.delete()
    return redirect('lista_mezzi')
def api_test(request):
    return render(request, 'api_test.html')



def lista_consegne_ricevute(request):
    notifiche = NotificaConsegna.objects.all().order_by("-ricevuta_il")
    return render(request, "consegne.html", {"notifiche": notifiche})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NotificaConsegna
import json

@csrf_exempt
def ricevi_assegnazione(request):
    if request.method == "POST":
        try:
            dati = json.loads(request.body)

            NotificaConsegna.objects.create(
                ordine_id=dati["ordine_id"],
                indirizzo=dati["indirizzo"],
                data_consegna=dati["data_consegna"],
                corriere=dati["corriere"]
            )

            return JsonResponse({"stato": "ok", "messaggio": "Consegna salvata"}, status=200)
        except Exception as e:
            return JsonResponse({"errore": str(e)}, status=400)
    else:
        return JsonResponse({"errore": "Metodo non consentito"}, status=405)

def visualizza_consegne(request):
    consegne = NotificaConsegna.objects.all().order_by('-ricevuta_il')  # più recenti prima
    return render(request, 'consegne.html', {'consegne': consegne})



