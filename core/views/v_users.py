from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from ..models import CarritoCompras

def login_view(request):
    if request.user != None:
        if request.user.groups.filter(name='Colaborador').exists():
            return redirect('CObras')
        elif request.user.groups.filter(name='Administrador').exists():
            return redirect('infoColab')
        else:
            return redirect('homeCli')
    else:
        return render(request, 'registration/register.html', {'msj':'Debe crear una cuenta'})

def register(request):
    aux = {
        'formReg':CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data = request.POST)
        if formulario.is_valid():
            user = formulario.save()
            grupo = Group.objects.get(name='Cliente')
            user.groups.add(grupo)
            carrito = CarritoCompras(cliente=user)
            carrito.save()
            return redirect(to='login')
        else:
            aux['form'] = formulario
            aux['msj'] = 'Ups, algo a salido mal'
            return render(request, 'registration/register.html', aux)
    else:
        return render(request, 'registration/register.html', aux)

def toLogin(request):
    return redirect(to="homeCli")

def bloqueado_por_ip(request):
    return render(request, 'core/Advertencia/bloquedo_por_ip.html')