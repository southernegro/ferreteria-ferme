import django_tables2 as tables
from .models import Profile

class ProfileTable(tables.Table):
    class Meta:
        model = Profile
        template_name = "django_tables2/bootstrap.html"
        fields = ("id","Nombre", "Apellido","Número de telefono","Correo Electronico", "Tipo de usuario")