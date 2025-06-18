# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Consegna
import requests

@receiver(post_save, sender=Consegna, weak=False)
def notifica_consegna_al_corriere(sender, instance, created, **kwargs):
    print(f"[Signal] post_save chiamato per Consegna id={instance.id}, created={created}")
    if not created:
        print("[Signal] Non è una nuova consegna, nessuna notifica inviata.")
        return

    # Recupera dati
    dati = {
        'ordine_id': instance.ordine.id,
        'indirizzo': instance.ordine.indirizzo,
        'corriere': instance.corriere.nome,
    }
    webhook_url = instance.corriere.webhook_url
    print(f"[Signal] Nuova consegna: invio webhook a {webhook_url} con payload: {dati}")

    # Invia webhook
    try:
        response = requests.post(webhook_url, json=dati)
        print(f"[Signal] Webhook inviato. Codice risposta: {response.status_code}")
        print(f"[Signal] Corpo risposta: {response.text}")
    except Exception as e:
        print(f"[Signal] ERRORE durante invio webhook: {e}")
notifica_consegna_al_corriere()