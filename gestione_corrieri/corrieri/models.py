from django.db import models
import requests

def geocode_address(address):
    """
    Dummy geocode function. Replace with actual geocoding logic or API call.
    Returns (latitude, longitude) tuple or (None, None) if not found.
    """
    # Example: always return None, None for now
    return None, None


# Create your models here.

# ordine ha le priorita viste come oggetto e lo stato 
class Ordine(models.Model):
    PRIORITA_CHOICES = [
        (10, "Alta"),
        (5, "Media"),
        (1, "Bassa"),
    ]
    STATO_CHOICES = [
        ("DA_ASSEGNARE", "Da Assegnare"),
        ("ASSEGNATO", "Assegnato"),
        ("TRANSITO", "In Transito"),
        ("IN_CONSEGNA", "In Consegna"),
        ("COMPLETATO", "Completato"),
    ]
    
    id_ordine = models.AutoField(primary_key=True)
    data_e_ora_ordine = models.DateField()
    indirizzo = models.CharField(max_length=100)
    stato = models.CharField(max_length=20, choices=STATO_CHOICES, default="DA_ASSEGNARE")
    priorita = models.IntegerField(choices=PRIORITA_CHOICES)
    peso = models.FloatField(default=0)
    volume = models.FloatField(default=0)
    latitudine = models.FloatField(null=True, blank=True)
    longitudine = models.FloatField(null=True, blank=True)  # <--- aggiunto qui

# la classe corriere con i suoi attributi da testo
class Corriere(models.Model):
    id_corriere = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    capacità_massima= models.IntegerField()
    posizione_attuale= models.CharField(max_length=100, default="Non specificata")
    latitudine = models.FloatField(null=True, blank=True)
    longitudine = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.nome
    def save(self, *args, **kwargs):
        if self.posizione_attuale and (not self.latitudine or not self.longitudine):
            lat, lon = geocode_address(self.posizione_attuale)
            if lat and lon:
                self.latitudine = lat
                self.longitudine = lon
        super().save(*args, **kwargs)

class Veicolo(models.Model):
    id_veicolo = models.AutoField(primary_key=True)
    Codice_Corriere= models.CharField(max_length=100)
    capacità_massima= models.IntegerField()
    Targa_mezzo= models.CharField(max_length=100)

class Consegna(models.Model):
    id_consegna = models.AutoField(primary_key=True)
    id_ordine = models.ForeignKey(Ordine, on_delete=models.CASCADE, related_name='consegna')
    id_corriere = models.ForeignKey(Corriere, on_delete=models.CASCADE, related_name='corriere')
    id_veicolo = models.ForeignKey(Veicolo, on_delete=models.CASCADE, related_name='veicolo')

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    ruolo = models.CharField(max_length=20, choices=[('ADMIN', 'Admin'), ('USER', 'User')], default='USER')

    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.email})"

class NotificaConsegna(models.Model):
    ordine_id = models.IntegerField()
    indirizzo = models.TextField()
    data_consegna = models.DateTimeField()
    corriere = models.CharField(max_length=100)
    ricevuta_il = models.DateTimeField(auto_now_add=True)

















