from corrieri.models import Ordine, Corriere, Veicolo, Consegna
from django.db.models import Sum
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_coords(indirizzo):
    geolocator = Nominatim(user_agent="gestione_corrieri_app", timeout=10)
    try:
        location = geolocator.geocode(indirizzo)
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Indirizzo non trovato: {indirizzo}")
            return None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Errore geocoding per '{indirizzo}': {e}")
        return None

def assegna_ordini():
    ordini_da_assegnare = Ordine.objects.filter(stato="DA_ASSEGNARE").order_by('-priorita', 'data_e_ora_ordine')
    corrieri = list(Corriere.objects.all())

    print(f"Ordini da assegnare: {ordini_da_assegnare.count()}")
    print(f"Corrieri disponibili: {len(corrieri)}")

    for ordine in ordini_da_assegnare:
        print(f"Valuto ordine {ordine.id_ordine} ({ordine.indirizzo})")

        migliore = None
        migliore_score = float('inf')

        coord_ordine = get_coords(ordine.indirizzo)
        if not coord_ordine:
            print("  -> Coordinate ordine non trovate, salto")
            continue

        for corriere in corrieri:
            peso_assegnato = Ordine.objects.filter(
                consegna__id_corriere=corriere,
                stato="ASSEGNATO"
            ).aggregate(tot=Sum('peso'))['tot'] or 0

            capacita_residua = corriere.capacità_massima - peso_assegnato
            print(f"  Corriere {corriere.nome} - Capacità residua: {capacita_residua}, peso ordine: {ordine.peso}")

            if capacita_residua < ordine.peso:
                print(f"    -> Corriere {corriere.nome} non ha capacità sufficiente")
                continue

            coord_corriere = get_coords(corriere.posizione_attuale)
            if not coord_corriere:
                print(f"    -> Coordinate corriere {corriere.nome} non trovate")
                continue

            distanza = geodesic(coord_ordine, coord_corriere).km
            score = distanza - capacita_residua * 0.01

            print(f"    -> Corriere {corriere.nome}: distanza={distanza:.2f} km, score={score:.2f}")

            if score < migliore_score:
                migliore = corriere
                migliore_score = score

        if migliore:
            print(f"Trovato corriere migliore: {migliore.nome}")
            veicolo = Veicolo.objects.filter(Codice_Corriere=migliore.nome).first()
            print(f"Veicolo trovato: {veicolo}")

            if not veicolo:
                print(f"Nessun veicolo per il corriere {migliore.nome}, salto")
                continue

            print(f"Assegno ordine {ordine.id_ordine} a {migliore.nome} con veicolo {veicolo.id_veicolo}")
            Consegna.objects.create(id_ordine=ordine, id_corriere=migliore, id_veicolo=veicolo)
            ordine.stato = "ASSEGNATO"
            ordine.save()
        else:
            print(f"Nessun corriere disponibile per ordine {ordine.id_ordine}")
