from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Profile, Cliente, Producto, Seller, Supplier, Employee, Boleta, Factura, OrdenCompra

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','last_name', 'phone_number', 'email']
        widgets={
            'name': forms.TextInput(attrs={'placeholder': 'Nombre...'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido...'}),
            'phone_numer': forms.TextInput(attrs={'placeholder': 'Telefono...'}),
        }

class ClientForm(ModelForm):
    class Meta:
        model = Cliente
        fields = []
class SellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = []
class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = []
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = []

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['name', 'price', 'despacho', 'fecha_exp', 
        'stock', 'critic_stock', 'image', 'proveedor', 'familia', 'tipo_producto']

class BoletaForm(ModelForm):
    class Meta:
        model = Boleta
        fields = ['order', 'n_boleta', 'vendedor', 'total']

class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        fields = ['order', 'n_factura', 'vendedor', 'total', 'rut', 'razon', 'giro']

class OrdenCompraForm(ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['remitente', 'fecha', 'enviado', 'proveedor', 'detalle']
        exclude = ['remitente', 'fecha', 'enviado',]