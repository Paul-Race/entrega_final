from django.shortcuts import render,redirect
from ..models import *
import requests
from django.core.paginator import Paginator
""" obras = Obra.objects.filter(estado=True)
    obras_destacadas = Obra.objects.filter(estado=True, es_destacado=True)
"""
def homeCliAPI(request):
    response = requests.get('http://127.0.0.1:8000/api/obra/')
    response2 = requests.get('https://digimon-api.vercel.app/api/digimon')
    obras = response.json()
    digimons = response2.json()
    
    #le paso una lista de objetos
    paginator = Paginator(digimons, 9) #Muestra 10 datos
    page_number = request.GET.get('page') #obtenemos la pagina
    page_obj = paginator.get_page(page_number)

    aux = {
        'obras':obras,
        'page_obj':page_obj
    }
    return render(request, 'core/ClienteAPI/homeCli.html', aux)
