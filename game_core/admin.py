from django.contrib import admin
from .models import PerfilJugador, Raza, Equipamiento, Personaje, Inventario, AuditoriaLog

admin.site.register(PerfilJugador)
admin.site.register(Raza)
admin.site.register(Equipamiento)
admin.site.register(Personaje)
admin.site.register(Inventario)
admin.site.register(AuditoriaLog)