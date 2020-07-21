from django.db import models
from django.contrib.auth.models import User

# Create your models here.
TIPO_USUARIO = (
('Cliente', 'Cliente'),
('Vendedor', 'Vendedor'),
('Proveedor', 'Proveedor'),
('Empleado', 'Empleado'),
('Administrator', 'Administrator')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    tipo = models.CharField(default='Cliente', max_length=50, choices=TIPO_USUARIO)

    def __str__(self):
        return self.name

class Cliente(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    client_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        perfil='Sin Perfil Asociado'
        if self.profile is None:
            return perfil
        else:
            return self.profile.name
    
    @property
    def is_client(self):
        cliente = False
        tipo = self.profile.tipo
        if (tipo == 'Cliente'):
            cliente = True
        else:
            cliente = False
        return cliente
    
class Seller(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    seller_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.profile.name
    
    @property
    def is_seller(self):
        seller = False
        tipo = self.profile.tipo
        if (tipo == 'Vendedor'):
            seller = True
        else:
            seller = False
        return seller

class Supplier(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    supplier_id = models.CharField(max_length=3, null=True)
    
    def __str__(self):
        return self.profile.name

    @property
    def is_supplier(self):
        supplier = False
        tipo = self.profile.tipo
        if (tipo == 'Proveedor'):
            supplier = True
        else:
            supplier = False
        return supplier

class Employee(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.profile.name
    
    @property
    def is_employee(self):
        employee = False
        tipo = self.profile.tipo
        if (tipo == 'Empleado'):
            employee = True
        else:
            employee = False
        return employee

class Administrator(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    admin_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.profile.name

    @property
    def is_admin(self):
        admin = False
        tipo = self.profile.tipo
        if (tipo == 'Administrator'):
            admin = True
        else:
            admin = False
        return admin

class FamiliaProducto(models.Model):
    id_familia = models.CharField(max_length=3,default=False, null=True, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class TipoProducto(models.Model):
    id_tipo = models.CharField(max_length=3, default=False, null=True, blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Producto(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    despacho = models.BooleanField(default=False, null=True, blank=True)
    fecha_exp = models.CharField(max_length=10,default='31/12/2020', null=True, blank=True)
    stock = models.IntegerField(default=0, null=True, blank=True)
    critic_stock = models.IntegerField(default=10, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    proveedor = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=False, blank=False, default=1)
    familia = models.ForeignKey(FamiliaProducto, on_delete=models.CASCADE, null=False, blank=False, default=1)
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.CASCADE, null=False, blank=False, default=1)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    @property
    def skuProducto(self):
        #sku_prod = ''
        cod_prov = '000'
        cod_fam = '000'
        cod_fecha_venc = '00000000'
        cod_prov = str(self.proveedor.supplier_id)
        cod_fam = str(self.familia.id_familia)
        cod_fecha_venc == '00000000'
        id_prod = str(self.id)
        sku_prod = id_prod+cod_prov+cod_fam+cod_fecha_venc
        self.sku = sku_prod
        return sku_prod

class Order(models.Model):
    usuario = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = True
        orderitems = self.orderitems_set.all()
        for i in orderitems:
            if i.product.despacho == True:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitems_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItems(models.Model):
    product = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    usuario = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address

class Boleta(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    n_boleta = models.CharField(max_length=200, null=False)
    vendedor = models.CharField(default="Tienda Ferme", max_length=200, null=False)
    total = models.CharField(max_length=200, null=False)

    def __str__(self):
        return 'Boleta: ' + self.n_boleta

class Factura(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    n_factura = models.CharField(max_length=200, null=False)
    vendedor = models.CharField(default="Tienda Ferme", max_length=200, null=False)
    total = models.CharField(max_length=200, null=False)
    rut = models.CharField(max_length=200, null=False)
    razon = models.CharField(max_length=200, null=False)
    giro = models.CharField(max_length=200, null=False)

    def __str__(self):
        return 'Factura: ' + self.n_factura


ordenCompra_status = (
    ('En espera', 'En espera'),
    ('Aprobado', 'Aprobado'),
    ('Rechazado', 'Rechazado')
)
   


class OrdenCompra(models.Model):
    remitente = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    enviado = models.BooleanField(default=False, null=True, blank=False)
    proveedor = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    detalle = models.TextField(max_length=200, null=True)
    status = models.CharField(max_length=50,null=False, blank=False,choices=ordenCompra_status,default='En espera')

    def __str__(self):
        return str(self.id)