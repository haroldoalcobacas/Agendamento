from django.conf import settings
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.forms import ValidationError
from django.core.validators import RegexValidator

from django.db import models
from medicos.models import Agenda


def validate_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        raise ValidationError("CPF inválido.")

class Cliente(models.Model):
    SEXO = (
        ("MAS", "Maculino"),
        ("FEM", "Feminino")
    )
    
    sexo = models.CharField(max_length=9, choices=SEXO,)
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O número precisa estar neste formato: \
                        '+99 99 9999-0000'.")

    telefone = models.CharField(verbose_name="Telefone",
                                validators=[phone_regex],
                                max_length=17, null=True, blank=True)
    
    
    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11,
        unique=True,
        validators=[validate_cpf]
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        verbose_name='Usuário', 
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f'{self.user.name}'
    
class Consulta(models.Model):
    agenda = OneToOneField(Agenda, on_delete=models.CASCADE, related_name='consulta')  # Garante um único cliente por agenda
    cliente = ForeignKey(Cliente, on_delete=models.CASCADE, related_name='consultas')

    def __str__(self):
        return f'{self.agenda} - {self.cliente}'
    
