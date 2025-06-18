from django.apps import AppConfig


class CorrieriConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'corrieri'
# corrieri/apps.py

from django.apps import AppConfig

class CorrieriConfig(AppConfig):
    name = 'corrieri'

    def ready(self):
        print("DEBUG: ready() chiamato")
        from .assegnazione import assegna_ordini
        assegna_ordini()
        print("DEBUG: assegna_ordini() eseguita")
