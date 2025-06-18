from django import forms
from .models import Ordine

class OrdineForm(forms.ModelForm):
    class Meta:
        model = Ordine
        fields = ['data_e_ora_ordine', 'indirizzo', 'stato', 'priorita', 'peso']