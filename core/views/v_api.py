from rest_framework import viewsets
from ..serializers import *
from ..models import *
from rest_framework.renderers import JSONRenderer

class TecnicaViewset(viewsets.ModelViewSet):
    queryset = Tecnica.objects.all()
    serializer_class = TecnicaSerializer
    renderer_classes = [JSONRenderer] #Esta linea es para que no aparezca el formulario, en su lugar solo aparecera el json

class ObraViewset(viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
    renderer_classes = [JSONRenderer] #Esta linea es para que no aparezca el formulario, en su lugar solo aparecera el json