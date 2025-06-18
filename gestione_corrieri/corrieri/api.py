from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Ordine, Corriere, Veicolo, Consegna
from serializers import OrdineSerializer

@api_view(['POST'])
def registra_ordine(request):
    serializer = OrdineSerializer(data=request.data)
    if serializer.is_valid():
        ordine = serializer.save()
        codice_assegnazione = f"ORD-{ordine.id_ordine}-{ordine.data_e_ora_ordine.strftime('%Y%m%d')}"
        ordine.codice_assegnazione = codice_assegnazione
        ordine.save()
        return Response({
            "id_ordine": ordine.id_ordine,
            "codice_assegnazione": codice_assegnazione
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def stato_ordine(request, codice_assegnazione):
    try:
        ordine = Ordine.objects.get(codice_assegnazione=codice_assegnazione)
        consegna = Consegna.objects.filter(id_ordine=ordine).first()
        corriere = consegna.id_corriere.nome if consegna else None
        mezzo = Veicolo.objects.filter(Codice_Corriere=consegna.id_corriere).first().targa if consegna else None
        return Response({
            "stato": ordine.stato,
            "corriere": corriere,
            "mezzo": mezzo,
            "data_arrivo_prevista": ordine.data_arrivo_prevista
        })
    except Ordine.DoesNotExist:
        return Response({"detail": "Ordine non trovato."}, status=404)

@api_view(['GET'])
def consegne_corriere(request, codice_corriere):
    try:
        corriere = Corriere.objects.get(codice_corriere=codice_corriere)
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
