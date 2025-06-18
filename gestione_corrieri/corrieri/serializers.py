from rest_framework import serializers
from .models import Ordine

class OrdineSerializer(serializers.ModelSerializer):
    data_e_ora_ordine = serializers.DateField(
        input_formats=['%Y-%m-%d', '%d/%m/%Y']
    )
    class Meta:
        model = Ordine
        fields = '__all__'