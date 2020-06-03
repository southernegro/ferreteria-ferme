import django_tables2 as tables
from .models import *

class ProfileTable(tables.Table):
    class Meta:
        model = Profile
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", )