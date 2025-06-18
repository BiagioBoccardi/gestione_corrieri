from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Ordine, Corriere, Veicolo, Consegna
from .serializers import OrdineSerializer

@api_view(['POST'])
def registra_ordine(request):
    serializer = OrdineSerializer(data=request.data)
    if serializer.is_valid():
        ordine = serializer.save()
        codice_assegnazione = f"ORD-{ordine.id_ordine}-{ordine.data_e_ora_ordine.strftime('%Y%m%d')}"
        # Se non hai il campo, puoi aggiungerlo al modello Ordine oppure restituirlo solo nella risposta
        return Response({
            "id_ordine": ordine.id_ordine,
            "codice_assegnazione": codice_assegnazione
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def stato_ordine(request, codice_assegnazione):
    try:
        # Ricava id_ordine dal codice_assegnazione
        # Esempio: ORD-12-20250615 → 12
        id_ordine = int(codice_assegnazione.split('-')[1])
        ordine = Ordine.objects.get(id_ordine=id_ordine)
        consegna = Consegna.objects.filter(id_ordine=ordine).first()
        corriere = consegna.id_corriere.nome if consegna else None
        mezzo = None
        if consegna and consegna.id_veicolo:
            mezzo = consegna.id_veicolo.Targa_mezzo
        data_arrivo_prevista = getattr(ordine, 'data_arrivo_prevista', None)
        return Response({
            "stato": ordine.stato,
            "corriere": corriere,
            "mezzo": mezzo,
            "data_arrivo_prevista": data_arrivo_prevista
        })
    except (Ordine.DoesNotExist, IndexError, ValueError):
        return Response({"detail": "Ordine non trovato."}, status=404)

@api_view(['GET'])
def consegne_corriere(request, codice_corriere):
    try:
        # codice_corriere può essere il nome o l'id, qui usiamo il nome
        corriere = Corriere.objects.get(nome=codice_corriere)
        consegne = Consegna.objects.filter(id_corriere=corriere)
        risultati = []
        for c in consegne:
            risultati.append({
                "id_ordine": c.id_ordine.id_ordine,
                "stato": c.id_ordine.stato,
                "indirizzo": c.id_ordine.indirizzo
            })
        return Response(risultati)
    except Corriere.DoesNotExist:
        return Response({"detail": "Corriere non trovato."}, status=404)