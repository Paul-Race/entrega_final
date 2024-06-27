from django.shortcuts import render, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden

def colab_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            return render(request, 'core/Advertencia/advertencia.html')

        grupo_cliente = Group.objects.get(name='Colaborador')
        if not request.user.groups.filter(name='Colaborador').exists():
            return render(request, 'core/Advertencia/advertencia.html')

        # Si el usuario está autenticado y pertenece al grupo 'Cliente', ejecutar la vista
        return view_func(request, *args, **kwargs)

    return _wrapped_view



@login_required
@colab_required
def CObras(request):
    aux = {
        'form': ObraForm(),
    }
    if request.method == 'POST':
        formulario = ObraForm(request.POST, request.FILES)
        if formulario.is_valid():
            obra = formulario.save(commit=False)
            obra.colaborador = request.user
            obra.save()
            messages.success(request, 'Obra guardada correctamente')
        else:
            aux['form'] = formulario
            messages.error(request, 'No se pudo almacenar')
    return render(request, 'core/Colaboradores/CObras.html', aux)



@login_required
@colab_required
def RObras(request):
    user = request.user
    obras = Obra.objects.filter(colaborador=user, fue_comprado=False)
    aux = {
        'obras':obras
    }
    return render(request, 'core/Colaboradores/RObras.html', aux)

@login_required
@colab_required
def UDObras(request, id):
    obra = Obra.objects.get(id=id)
    aux = {
        'form': AObraForm(instance=obra),
        'obra': obra
    }
    if request.method == 'POST':
        formulario = AObraForm(data=request.POST, instance=obra, files=request.FILES)
        if formulario.is_valid():
            obraform = formulario.save(commit=False)
            obraform.estado = False
            obraform.save()
            aux['form'] = formulario
            messages.success(request, 'Obra actualizada correctamente')
        else:
            aux['form'] = formulario
            messages.error(request, 'No se pudo almacenar')
    return render(request, 'core/Colaboradores/UDObras.html', aux)

@login_required
@colab_required
def DObras(request, id):
    obra = Obra.objects.get(id=id)
    obra.delete()
    return redirect(to='RObras')

@login_required
@colab_required
def msjLeido(request, id):
    obra = Obra.objects.get(id=id)
    obra.delete()
    return redirect(to='CObras')
