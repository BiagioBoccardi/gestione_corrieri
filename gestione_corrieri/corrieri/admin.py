from django.contrib import admin
from corrieri.models import Ordine, Corriere , Veicolo, Consegna

# Register your models here.
admin.site.register(Ordine)
admin.site.register(Corriere)
admin.site.register(Veicolo)
admin.site.register(Consegna)
