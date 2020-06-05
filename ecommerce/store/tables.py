import django_tables2 as tables
from .models import Profile
from django_tables2.utils import A


TEMPLATE_EDIT = '''
    <div>
        <row>
            <button href={% url 'edit_user' record.pk %} type="button" class="btn btn-info btn-sm col-12 tbl_icon edit">Editar</button>
        </row>
    </div>
'''

TEMPLATE_DELETE = '''
    <div>
        <row>
            <button href={% url 'delete_user' record.pk %} type="button" class="btn btn-danger btn-sm col-12 tbl_icon edit">Borrar</button>
        </row>
    </div>
'''
class ProfileTable(tables.Table):
    Editar = tables.TemplateColumn(TEMPLATE_EDIT)
    Borrar = tables.TemplateColumn(TEMPLATE_DELETE)
    class Meta:
        model = Profile
        template_name = "django_tables2/bootstrap.html"