from django.urls import path
from . import views

urlpatterns = [
    # URLs para Campistas
    path('', views.index, name='index'),
    path('campistas/', views.listado_campistas, name='listado_campistas'),
    path('campistas/nuevo/', views.nuevo_campista, name='nuevo_campista'),
    path('campistas/<int:campista_id>/', views.detalle_campista, name='detalle_campista'),
    path('campistas/<int:campista_id>/editar/', views.editar_campista, name='editar_campista'),
    path('campistas/<int:campista_id>/eliminar/', views.eliminar_campista, name='eliminar_campista'),
    
    # URLs para Reservas
    path('reservas/', views.listado_reservas, name='listado_reservas'),
    path('reservas/nueva/', views.nueva_reserva, name='nueva_reserva'),
    path('reservas/<int:reserva_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('reservas/<int:reserva_id>/editar/', views.editar_reserva, name='editar_reserva'),
    path('reservas/<int:reserva_id>/eliminar/', views.eliminar_reserva, name='eliminar_reserva'),
]
