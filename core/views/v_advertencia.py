from django.shortcuts import render,redirect

def advertencia(request):
    return render(request, 'core/Advertencia/advertencia.html')