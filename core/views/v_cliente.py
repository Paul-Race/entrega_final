from datetime import datetime
from django.shortcuts import render,redirect
from ..models import *
from ..forms import TecnicaForm, FiltroForm
from django.contrib import messages
from django.contrib.auth.models import Group
import requests
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def cliente_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si el usuario está autenticado
        if not request.user.is_authenticated:
            return render(request, 'core/Advertencia/advertencia.html')

        grupo_cliente = Group.objects.get(name='Cliente')
        if not request.user.groups.filter(name='Cliente').exists():
            return render(request, 'core/Advertencia/advertencia.html')

        # Si el usuario está autenticado y pertenece al grupo 'Cliente', ejecutar la vista
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def homeCli(request):
    carrito = None
    cantidad_carrito = 0
    if request.user.is_authenticated:
        carrito = CarritoCompras.objects.get(cliente=request.user)
        cantidad_carrito = carrito.obras.all().count()

    obras = Obra.objects.filter(estado=True, fue_comprado=False)
    obras_destacadas = Obra.objects.filter(estado=True, es_destacado=True, fue_comprado=False)
        #le paso una lista de objetos
    paginator = Paginator(obras, 9) #Muestra 10 datos
    page_number = request.GET.get('page') #obtenemos la pagina
    page_obj = paginator.get_page(page_number)

    aux = {
        'page_obj':page_obj,
        'obras_desc': obras_destacadas,
        'form':FiltroForm(),
        'cantidad_carrito': cantidad_carrito,
        'carrito':carrito,
    }
    if request.method == 'POST':
        form = FiltroForm(request.POST)
        if form.is_valid():
            tecnica = form.cleaned_data.get('tecnica')
            if tecnica is not None:
                obras = Obra.objects.filter(estado=True, fue_comprado=False)
                obras = obras.filter(tecnica=tecnica)
                paginator = Paginator(obras, 9) #Muestra 10 datos
                page_obj = paginator.get_page(page_number)
                aux['page_obj'] = page_obj
            return render(request, 'core/Cliente/homeCli.html', aux)
    return render(request, 'core/Cliente/homeCli.html', aux)

def verObra (request, id):
    obra = Obra.objects.get(id=id)
    aux = {
        'obra':obra
    }

    return render(request, 'core/Cliente/verObra.html',aux)

@login_required
@cliente_required
def pagar(request, id):
    obra = Obra.objects.get(id=id)
    obra.delete()
    return redirect(to='homeCli')

@login_required
@cliente_required
def agregarCarrito(request, id):
    obra = Obra.objects.get(id=id)
    carrito = CarritoCompras.objects.get(cliente=request.user)
    carrito.obras.add(obra)
    carrito.save()
    messages.success(request, '¡Producto agregado al carrito!')
    return redirect(to='homeCli')

@login_required
@cliente_required
def eliminarCarrito(request, id):
    obra = Obra.objects.get(id=id)
    carrito = CarritoCompras.objects.get(cliente=request.user)
    carrito.obras.remove(obra)
    carrito.save()
    messages.success(request, '¡Producto eliminado del carrito!')
    return redirect(to='verCarrito')

@login_required
@cliente_required
def verCarrito(request):
    carrito = CarritoCompras.objects.get(cliente=request.user)
    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime("%d-%m-%Y")
    response = requests.get(f"https://mindicador.cl/api/dolar/{fecha_formateada}")
    response2 = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    datos = response.json()
    datos2 = response2.json()
    dolar = datos['serie'][0]['valor']
    bitcoin = datos2['bpi']['USD']['rate']
    print(dolar)
    print(bitcoin)
    obras = carrito.obras.all()
    acumulador = 0
    for obra in obras:
        acumulador += obra.precio

    aux = {
        'carrito':carrito,
        'total':acumulador,
        'dolar':dolar,
        'bitcoin':bitcoin
        }
    
    return render(request, 'core/Cliente/verCarrito.html', aux)

@login_required
@cliente_required
def pagarCarrito(request, total):
    carrito = CarritoCompras.objects.get(cliente=request.user)
    compra = Compra(cliente=request.user)
    obras = carrito.obras.all()
    lista_obras = []
    lista_precio = []
    for obra in obras:
        compra.obras.add(obra)
        obra.fue_comprado = True
        obra.cliente = request.user
        obra.save()
        lista_obras.append(obra.titulo)
        lista_precio.append(obra.precio)
    compra.save()
    mensaje = ""
    for x in range(len(lista_obras)):
        mensaje += f"Nombre: {lista_obras[x]} Precio: ${lista_precio[x]} "

    messages.success(request, f'¡Comprado con éxito! ud pago el total de ${total} USD por {len(lista_precio)} productos, {mensaje}')
    carrito.obras.clear()
    return redirect(to='homeCli')

def misCompras(request):
    compras = Compra.objects.filter(cliente=request.user)
    obras = Obra.objects.filter(fue_comprado=True, cliente=request.user)
    aux = {
        'compras':compras,
        'obras':obras
    }
    return render(request, 'core/Cliente/misCompras.html', aux)

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def generar_pdf(request, compra_id):
    # Obtener la compra
    compra = Compra.objects.get(id=compra_id)
    
    # Crear un archivo en memoria
    buffer = io.BytesIO()
    
    # Crear el objeto PDF usando ReportLab
    p = canvas.Canvas(buffer)
    
    # Agregar contenido al PDF
    p.drawString(100, 800, f"Fecha de compra: {compra.fecha_compra}")
    y = 780
    total = 0
    for obra in compra.obras.all():
        p.drawString(100, y, f"Obra: {obra.titulo} - ${obra.precio}")
        total += obra.precio
        y -= 20
    
    p.drawString(100, y, f"Total: ${total}")
    
    # Cerrar el PDF
    p.showPage()
    p.save()
    
    # Regresar el archivo PDF como respuesta
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='compra.pdf')

#Validar que este logueado para entrar aqui


