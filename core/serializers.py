from rest_framework import serializers
from .models import *

class TecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnica
        fields = '__all__'
        
class ObraSerializer(serializers.ModelSerializer):
    tecnica = TecnicaSerializer(read_only=True)
    class Meta:
        model = Obra
        fields = '__all__'