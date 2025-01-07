from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm, NotasForm
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Nota
from django.contrib.auth.decorators import login_required

@login_required
def CrearNotas(req: HttpResponse):
    if req.method == 'POST':
        nota = NotasForm(req.POST)
        if nota.is_valid():
            nuevanota = Nota(
                titulo = nota.cleaned_data['titulo'],
                descripcion = nota.cleaned_data['descripcion'],
                finalizada = nota.cleaned_data['finalizada'],
                usuario = req.user
            )
            nuevanota.save()
            return redirect('Mis Notas')
        else:
            return render(req, 'index.html', {'mensaje': 'Nota Inválida. Intente nuevamente rellenando como se indica en el formulario.'})
    else:
        form = NotasForm()
    return render(req, 'index.html', {'form': form})

@login_required
def MisNotas(req):
    notas = Nota.objects.filter(usuario=req.user)
    return render(req, 'misnotas.html', {'notas': notas})


def Registrarse(req):
    if req.method == 'POST':
        form = RegistroForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            messages.success(req, "Registro completado con éxito. ¡Bienvenido!")
            return redirect('Crear Notas')
        else:
            messages.error(req, "Por favor, corrige los errores a continuación.")
    else:
        form = RegistroForm()
    
    return render(req, 'registrarse.html', {'form': form})


def IniciarSesion(req):
    if req.method == 'POST':
        form = AuthenticationForm(data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('Crear Notas')
            else:
                messages.error(req, "Usuario o contraseña incorrectos.")
        else:
            messages.error(req, "Formulario no válido.")
    else:
        form = AuthenticationForm()
    return render(req, 'iniciarsesion.html', {'form': form})

@login_required
def CerrarSesion(req):
    logout(req)
    messages.success(req, "Has cerrado sesión correctamente.")
    return redirect('Iniciar Sesion')


def EliminarNota(req, idnota):
    if req.method == 'POST':
        try:
            nota = Nota.objects.get(id=idnota, usuario=req.user)
            nota.delete()
            messages.success(req, "Nota eliminada correctamente.")

        
        except Nota.DoesNotExist:
            messages.error(req, "La nota no existe.")
        
        return redirect('Mis Notas')
    else:
        return redirect('Mis Notas')

@login_required
def EditarNota(req, idnota):
    try:
        nota = Nota.objects.get(id=idnota, usuario=req.user)
    except Nota.DoesNotExist:
        messages.error(req, "La nota no existe o no tienes permisos para editarla.")
        return redirect('Mis Notas')

    if req.method == 'POST':
        form = NotasForm(req.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(req, "Nota actualizada correctamente.")
            return redirect('Mis Notas')
        else:
            messages.error(req, "Formulario inválido. Por favor, corrige los errores.")
    else:
        form = NotasForm(instance=nota)

    return render(req, 'editarnota.html', {'form': form, 'nota': nota})
