from django.shortcuts import render,redirect
from ..models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib import messages
from ..forms import MsjObraForm
from django.db.models import Count, Q

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            return render(request, 'core/Advertencia/advertencia.html')

        grupo_cliente = Group.objects.get(name='Administrador')
        if not request.user.groups.filter(name='Administrador').exists():
            return render(request, 'core/Advertencia/advertencia.html')

        # Si el usuario está autenticado y pertenece al grupo 'Cliente', ejecutar la vista
        return view_func(request, *args, **kwargs)

    return _wrapped_view

@login_required
@admin_required
def infoColab(request):
    colaboradores_con_obras = User.objects.annotate(
        num_obras=Count('obra'),
        num_obras_aprobadas=Count('obra', filter=Q(obra__estado=True, obra__fue_comprado=False)),
        num_obras_pendientes=Count('obra', filter=Q(obra__estado=False, obra__mensaje=None, obra__fue_comprado=False))
    ).filter(num_obras__gt=0)
    aux = {
        'colab': colaboradores_con_obras,
    }
    return render(request, 'core/Admin/infoColabdres.html', aux)

def obrasColab(request, id):
    obras = Obra.objects.filter(colaborador_id=id, estado=True, fue_comprado=False)
    vendedor = User.objects.get(id=id)
    aux = {
        'obras': obras,
        'colab':vendedor
    }
    return render(request, 'core/Admin/obrasColab.html', aux)


@login_required
@admin_required
def peticiones(request):
    obras = Obra.objects.filter(estado=False, fue_comprado=False)
    aux = {
        'obras':obras
    }
    return render(request, 'core/Admin/peticiones.html', aux)

@login_required
@admin_required
def aprobarObra(request, id):
    obra = Obra.objects.get(id=id)
    obra.estado = True
    obra.save()
    return redirect(to='peticiones')


@login_required
@admin_required
def eliminar(request, id):
    obra = Obra.objects.get(id=id)
    obra.delete()
    return redirect(to='infoColab')

@login_required
@admin_required
def rechazar(request, id):
    print("Vista rechazar llamada")
    obra = Obra.objects.get(id=id)
    aux = {
        'form':MsjObraForm(instance=obra),
        'obra':obra
    }
    if request.method == 'POST':
        form = MsjObraForm(request.POST, instance=obra)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha rechazado la obra correctamente')
            return redirect(to='peticiones')
        else:
            messages.error(request, 'Por favor, indique un motivo para rechazar la obra')
    return render(request, 'core/Admin/rechazarObra.html', aux)

from django.db.models import Count

def estadisticas(request):
    #Cuantas obras a vendido cada colaborador
    #x.colaborador x.totalvendido
    colaboradores = Obra.objects.filter(fue_comprado=True).values('colaborador').annotate(total_vendido=Count('colaborador')).order_by('-total_vendido')    
    obras = Obra.objects.filter(fue_comprado=True).order_by('id')
    ids_colaboradores = [colaborador['colaborador'] for colaborador in colaboradores]
    usuarios = User.objects.filter(id__in=ids_colaboradores)
    conteo_pintura = 0
    conteo_escultura = 0
    conteo_ceramica = 0
    for x in obras:
        if x.tecnica.descripcion == 'Pintura':
            conteo_pintura += 1
        if x.tecnica.descripcion == 'Escultura':
            conteo_escultura += 1
        if x.tecnica.descripcion == 'Ceramica':
            conteo_ceramica += 1
    acumulador = 0
    contador = 0
    for x in obras:
        contador += 1
        acumulador += x.precio
    total_dinero = acumulador
    total_ventas = contador
    try:
        promedio_por_venta = acumulador / contador
    except ZeroDivisionError:
        promedio_por_venta = 0
    aux = {
        'colaboradores':colaboradores,
        'conteo_pintura':conteo_pintura,
        'conteo_escultura':conteo_escultura,
        'conteo_ceramica':conteo_ceramica,
        'total_dinero':total_dinero,
        'total_ventas':total_ventas,
        'promedio_por_venta':promedio_por_venta,
        'usuarios':usuarios
    }
    return render(request, 'core/Admin/estadisticas.html', aux)
