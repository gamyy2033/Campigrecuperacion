from django.db import models

class Campista(models.Model):
    nombre_completo = models.CharField(max_length=150)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField(blank=True, null=True)  # Opcional

    def __str__(self):
        return self.nombre_completo


class Reserva(models.Model):
    TIPO_ALOJAMIENTO_OPCIONES = [
        ('Tienda', 'Tienda'),
        ('Cabaña', 'Cabaña'),
        ('Caravana', 'Caravana'),
    ]

    ESTADO_RESERVA_OPCIONES = [
        ('Confirmada', 'Confirmada'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada'),
    ]

    campista = models.ForeignKey(Campista, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_alojamiento = models.CharField(max_length=20, choices=TIPO_ALOJAMIENTO_OPCIONES)
    numero_personas = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO_RESERVA_OPCIONES, default='Pendiente')
    observaciones = models.TextField(blank=True, null=True)  # Opcional

    def __str__(self):
        return f"Reserva de {self.campista.nombre_completo} ({self.fecha_inicio} - {self.fecha_fin})"
