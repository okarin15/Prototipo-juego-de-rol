from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from cryptography.fernet import Fernet

# Generamos clave de cifrado simétrico para proteger los datos
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# --- ESTADO SEGURO: Datos protegidos ---
class PerfilJugador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    # Aumentamos a 255 porque el texto cifrado es mucho más largo que el original
    rut = models.CharField(max_length=255, help_text="Formato: 12.345.678-9")
    telefono = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Si el RUT existe y NO está cifrado aún (los cifrados con Fernet empiezan con gAAAAA)
        if self.rut and not self.rut.startswith('gAAAAA'):
            self.rut = cipher_suite.encrypt(self.rut.encode('utf-8')).decode('utf-8')
            
        if self.telefono and not self.telefono.startswith('gAAAAA'):
            self.telefono = cipher_suite.encrypt(self.telefono.encode('utf-8')).decode('utf-8')
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

# --- CATÁLOGOS Y ENTIDADES DEL RPG ---
class Raza(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    bono_fuerza = models.IntegerField(default=0)
    bono_agilidad = models.IntegerField(default=0)
    bono_inteligencia = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Equipamiento(models.Model):
    TIPO_CHOICES = [('arma', 'Arma'), ('armadura', 'Armadura'), ('consumible', 'Consumible')]
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    puntos_ataque = models.IntegerField(default=0)
    puntos_defensa = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Personaje(models.Model):
    ESTADOS_PERMITIDOS = [('vivo', 'Vivo'), ('muerto', 'Muerto')]
    jugador = models.ForeignKey(User, on_delete=models.CASCADE)
    raza = models.ForeignKey(Raza, on_delete=models.RESTRICT, null=True)
    nombre = models.CharField(max_length=60, unique=True)
    nivel = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    estado_vital = models.CharField(max_length=20, choices=ESTADOS_PERMITIDOS, default='vivo')
    
    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE)
    equipamiento = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

class AuditoriaLog(models.Model):
    fecha_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    accion = models.CharField(max_length=100)
    recurso_afectado = models.CharField(max_length=100)