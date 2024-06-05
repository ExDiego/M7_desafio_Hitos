from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import SolicitudArriendo, Propiedad, Region, Comuna
from .forms import CustomUserChangeForm, RegistroUsuarioForm, SolicitudArriendoForm, PropiedadForm
# Create your views here.



def index(request):
    propiedades = Propiedad.objects.all()
    return render(request, 'index.html', {'propiedades': propiedades}) 

@login_required
def detalle_propiedad(request, id):
    propiedad = Propiedad.objects.get (pk=id)
    return render(request,'detalle_propiedad.html',{'propiedad': propiedad })

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        print(form)
        if form.is_valid():
            usuario = form.save(commit=False)
            password = form.cleaned_data['password']
            usuario.set_password(password)
            usuario.save()
            # Autenticar al usuario después del registro
            usuario_autenticado = authenticate(username=usuario.username, password=password)
            if usuario_autenticado is not None:
                login(request, usuario_autenticado)
                return redirect('index')  
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro_usuario.html', {'form': form})

@login_required
def generar_solicitud_arriendo(request, id):
    # Obtener propiedad por su id
    propiedad = get_object_or_404(Propiedad, pk=id)
    
    # Verificar si el usuario está autenticado y es un arrendatario
    if request.user.is_authenticated and request.user.usuario.tipo_usuario == 'arrendatario':
        if request.method == 'POST':
            form = SolicitudArriendoForm(request.POST)
            if form.is_valid():
                solicitud = form.save(commit=False)
                solicitud.arrendatario = request.user.usuario  # Asignar el usuario arrendatario
                solicitud.propiedad = propiedad
                solicitud.save()
                return redirect('detalle', id=propiedad.id)
        else:
            # Inicializar el formulario con la propiedad correspondiente
            form = SolicitudArriendoForm(initial={'propiedad': propiedad})
        return render(request, 'generar_solicitud_arriendo.html', {'form': form})
    else:
        return redirect('index')
    

@login_required
def solicitudes_arrendador(request):
    # Verificar si el usuario es un arrendador
    if request.user.usuario.tipo_usuario == 'arrendatario':
        # Obtener todas las solicitudes recibidas por el arrendador
        solicitudes = SolicitudArriendo.objects.filter(propiedad__propietario=request.user)
        return render(request, 'solicitudes_arrendatario.html', {'solicitudes': solicitudes})
    else:
        # Redirigir a otra página si el usuario no es un arrendador
        return redirect('index')  


@login_required
def crear_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            propiedad = form.save(commit=False)
            propiedad.propietario = request.user
            propiedad.save()
            return redirect('dashboard') 
    else:
        form = PropiedadForm()
    return render(request, 'alta_propiedad.html', {'form': form})


@login_required
def actualizar_propiedad(request, id):
    propiedad = get_object_or_404(Propiedad, pk=id)
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES, instance=propiedad)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PropiedadForm(instance=propiedad)
    return render(request, 'editar_propiedad.html',{'form':form })

@login_required
def eliminar_propiedad(request, id):
    propiedad = get_object_or_404(Propiedad, pk=id)
    if request.method == 'POST':
        propiedad.delete()
        return redirect('dashboard')
    else:
        return render(request,'eliminar_propiedad.html', {'propiedad':propiedad} )


@login_required
def dashboard(request):
    if request.user.tipo_usuario == 'arrendatario':
        solicitudes = SolicitudArriendo.objects.filter(arrendatario=request.user)
        regiones = Region.objects.all()
        comunas = Comuna.objects.all()
        region_id = request.GET.get('region')
        comuna_id = request.GET.get('comuna')
        propiedades = Propiedad.objects.all()
        if region_id:
            propiedades = propiedades.filter(comuna__region_id=region_id)
        if comuna_id:
            propiedades = propiedades.filter(comuna_id=comuna_id)
        
        return render(request, 'dashboard_arrendatario.html', {'solicitudes': solicitudes, 'regiones': regiones, 'comunas': comunas, 'propiedades': propiedades})
    
    elif request.user.tipo_usuario == 'arrendador':
        # Obtener las solicitudes recibidas por el arrendador
        solicitudes_recibidas = SolicitudArriendo.objects.filter(propiedad__propietario=request.user)
        # Obtener las propiedades del arrendador
        propiedades = Propiedad.objects.filter(propietario=request.user)
        return render(request, 'dashboard_arrendador.html', {'solicitudes_recibidas': solicitudes_recibidas, 'propiedades': propiedades})   
    
    
@login_required
def actualizar_usuario(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user.usuario)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Los datos del usuario han sido actualizados!')
            return redirect('dashboard') 
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'perfil.html', {'form': form})    