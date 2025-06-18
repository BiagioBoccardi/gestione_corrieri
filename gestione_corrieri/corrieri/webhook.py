import requests
from models import Ordine
from assegnazione import assegna_ordini

def invia_webhook_assegnazione(ordine):
    url = "https://endpoint-corriere.com/webhook"
    payload = {
        "ordine": ordine.codice_spedizione,
        "corriere": ordine.corriere_assegnato.nome,
        "mezzo": ordine.mezzo_assegnato.codice,
        "indirizzo": ordine.indirizzo,
        "data": ordine.data_consegna.isoformat(),
    }
    requests.post(url, json=payload)