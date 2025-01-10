from django.shortcuts import render, get_object_or_404, redirect
from .models import Campista, Reserva
import re
from datetime import date
from django.utils import timezone

# Página de inicio
def index(request):
    return render(request, 'index.html')

# Listar campistas

def listado_campistas(request):
    # Obtener el término de búsqueda (si existe)
    search_query = request.GET.get('search', '')
    
    # Filtrar los campistas si se proporciona un término de búsqueda
    if search_query:
        campistas = Campista.objects.filter(nombre_completo__icontains=search_query)
    else:
        campistas = Campista.objects.all()
    
    # Pasar los campistas a la plantilla
    return render(request, 'listado_campistas.html', {'campistas': campistas, 'search': search_query})

# Crear nuevo campista

def nuevo_campista(request):
    if request.method == 'POST':
        nombre_completo = request.POST['nombre_completo']
        correo_electronico = request.POST['correo_electronico']
        telefono = request.POST['telefono']
        direccion = request.POST.get('direccion', '')

        # Lista para acumular errores
        errores = []

        # Validación del nombre completo: solo letras
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre_completo):
            errores.append('El nombre completo solo debe contener letras.')

        # Validación del teléfono: 10 dígitos y empieza con "0"
        if not re.match(r'^0\d{9}$', telefono):
            errores.append('El teléfono debe tener 10 dígitos y empezar con "0".')

        # Validación de unicidad del correo electrónico
        if Campista.objects.filter(correo_electronico=correo_electronico).exists():
            errores.append('El correo electrónico ya está registrado.')

        # Si hay errores, mostramos todos en el formulario
        if errores:
            return render(request, 'nuevo_campista.html', {
                'errores': errores,
                'nombre_completo': nombre_completo,
                'correo_electronico': correo_electronico,
                'telefono': telefono,
                'direccion': direccion,
            })

        try:
            # Crear el campista si no hay errores
            Campista.objects.create(
                nombre_completo=nombre_completo,
                correo_electronico=correo_electronico,
                telefono=telefono,
                direccion=direccion,
            )
            return redirect('listado_campistas')
        except IntegrityError:
            errores.append('Ocurrió un error al guardar el campista. Intenta nuevamente.')
            return render(request, 'nuevo_campista.html', {
                'errores': errores,
                'nombre_completo': nombre_completo,
                'correo_electronico': correo_electronico,
                'telefono': telefono,
                'direccion': direccion,
            })

    return render(request, 'nuevo_campista.html')
# Detalles de un campista
def detalle_campista(request, campista_id):
    campista = get_object_or_404(Campista, id=campista_id)
    return render(request, 'detalle_campista.html', {'campista': campista})

# Editar campista

def editar_campista(request, campista_id):
    campista = get_object_or_404(Campista, id=campista_id)
    if request.method == 'POST':
        nombre_completo = request.POST['nombre_completo']
        correo_electronico = request.POST['correo_electronico']
        telefono = request.POST['telefono']
        direccion = request.POST.get('direccion', '')

        # Lista para acumular errores
        errores = []

        # Validación del nombre (no debe contener números)
        if any(char.isdigit() for char in nombre_completo):
            errores.append('El nombre completo no puede contener números.')

        # Validación del correo electrónico (debe contener '@')
        if '@' not in correo_electronico:
            errores.append('El correo electrónico debe contener "@" y ser un formato válido.')

        # Validación del teléfono (debe empezar con '0' y tener 10 dígitos)
        if not re.match(r'^0\d{9}$', telefono):
            errores.append('El teléfono debe comenzar con "0" y contener 10 dígitos.')

        # Si hay errores, mostrarlos en el formulario
        if errores:
            return render(request, 'editar_campista.html', {
                'errores': errores,
                'campista': campista
            })

        # Si no hay errores, actualizar el campista
        campista.nombre_completo = nombre_completo
        campista.correo_electronico = correo_electronico
        campista.telefono = telefono
        campista.direccion = direccion
        campista.save()

        return redirect('listado_campistas')

    return render(request, 'editar_campista.html', {'campista': campista})
# Eliminar campista
def eliminar_campista(request, campista_id):
    campista = get_object_or_404(Campista, id=campista_id)
    if request.method == 'POST':
        campista.delete()
        return redirect('listado_campistas')
    return render(request, 'eliminar_campista.html', {'campista': campista})


# Listar reservas
def listado_reservas(request):
    # Obtener el término de búsqueda (si existe) desde la solicitud
    search_query = request.GET.get('search', '')
    
    # Filtrar las reservas si se proporcionó un término de búsqueda
    if search_query:
        reservas = Reserva.objects.filter(
            campista__nombre_completo__icontains=search_query
        ) | Reserva.objects.filter(
            fecha_inicio__icontains=search_query
        ) | Reserva.objects.filter(
            fecha_fin__icontains=search_query
        )
    else:
        reservas = Reserva.objects.all()
    
    return render(request, 'listado_reservas.html', {'reservas': reservas})

# Crear nueva reserva

def nueva_reserva(request):
    if request.method == 'POST':
        campista_id = request.POST['campista']
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        tipo_alojamiento = request.POST['tipo_alojamiento']
        numero_personas = request.POST['numero_personas']
        estado = request.POST['estado']
        observaciones = request.POST.get('observaciones', '')

        # Lista para acumular errores
        errores = []

        # Validación de que la fecha de inicio no sea antes de hoy
        hoy = date.today()
        try:
            fecha_inicio_obj = date.fromisoformat(fecha_inicio)
            if fecha_inicio_obj < hoy:
                errores.append('La fecha de inicio no puede ser anterior a hoy.')
        except ValueError:
            errores.append('La fecha de inicio es inválida.')

        # Validación de que la fecha de fin sea posterior a la fecha de inicio
        try:
            fecha_fin_obj = date.fromisoformat(fecha_fin)
            if fecha_inicio_obj > fecha_fin_obj:
                errores.append('La fecha de fin debe ser posterior o igual a la fecha de inicio.')
        except ValueError:
            errores.append('La fecha de fin es inválida.')

        # Validación del número de personas
        if not numero_personas.isdigit() or int(numero_personas) <= 0:
            errores.append('El número de personas debe ser un número positivo.')

        # Validación del campista (asegurarse de que existe)
        if not Campista.objects.filter(id=campista_id).exists():
            errores.append('El campista seleccionado no existe.')

        # Si hay errores, mostramos todos en el formulario
        if errores:
            return render(request, 'nueva_reserva.html', {
                'errores': errores,
                'campistas': Campista.objects.all(),
                'campista_id': campista_id,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'tipo_alojamiento': tipo_alojamiento,
                'numero_personas': numero_personas,
                'estado': estado,
                'observaciones': observaciones,
            })

        # Crear la reserva si no hay errores
        Reserva.objects.create(
            campista_id=campista_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_alojamiento=tipo_alojamiento,
            numero_personas=numero_personas,
            estado=estado,
            observaciones=observaciones,
        )
        return redirect('listado_reservas')

    # Obtener campistas para el formulario
    return render(request, 'nueva_reserva.html', {
        'campistas': Campista.objects.all(),
    })
# Detalles de una reserva
def detalle_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'detalle_reserva.html', {'reserva': reserva})

# Editar reserva


def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    campistas = Campista.objects.all()

    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        # Validación de que la fecha de inicio no sea anterior a hoy
        hoy = timezone.now().date()
        if fecha_inicio < str(hoy):
            # Si la fecha de inicio es antes de hoy, agregar un error
            return render(request, 'editar_reserva.html', {
                'reserva': reserva,
                'campistas': campistas,
                'error_fecha_inicio': 'La fecha de inicio no puede ser anterior a hoy.'
            })
        
        # Si la validación pasa, actualizar los datos de la reserva
        reserva.fecha_inicio = fecha_inicio
        reserva.fecha_fin = request.POST['fecha_fin']
        reserva.tipo_alojamiento = request.POST['tipo_alojamiento']
        reserva.numero_personas = request.POST['numero_personas']
        reserva.estado = request.POST['estado']
        reserva.observaciones = request.POST.get('observaciones', '')
        reserva.save()
        return redirect('listado_reservas')

    return render(request, 'editar_reserva.html', {'reserva': reserva, 'campistas': campistas})

# Eliminar reserva
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        reserva.delete()
        return redirect('listado_reservas')
    return render(request, 'eliminar_reserva.html', {'reserva': reserva})
