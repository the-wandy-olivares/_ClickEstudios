from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Profile(models.Model):
      ROLE_CHOICES = [
            ('estandard', 'Estandar'),
            ('administrativo', 'Administrativo'),
            ('administrador', 'Administrador'),
      ]
      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True, null=True)
      phone = models.CharField(max_length=15, blank=True, null=True)
      address = models.TextField(blank=True, null=True)
      img = models.ImageField(upload_to='media/profile', null=True, blank=True)
      role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='estandard')
      estudio = models.ForeignKey('Estudios', on_delete=models.CASCADE, related_name='profile_estudios', null=True, blank=True)

      def __str__(self):
            return f"{self.user.first_name} {self.user.last_name} - {self.get_role_display()}"

class Empleado(models.Model):
      ROLE_CHOICES = [
            ('estandard', 'Estandar'),
            ('administrativo', 'Administrativo'),
            ('administrador', 'Administrador'),
      ]

      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='empleado', default=1)
      estudio = models.ForeignKey('Estudios', on_delete=models.CASCADE, related_name='empleados', null=True, blank=True)
      name = models.CharField(max_length=100, blank=False, null=False)
      img = models.ImageField(upload_to='media/empleados', null=True, blank=True)
      role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='estandard')
      date_joined = models.DateTimeField(auto_now_add=True)
      is_active = models.BooleanField(default=True)

      class Meta:
            verbose_name = 'empleado'
            verbose_name_plural = 'empleados'

      def __str__(self):
            return f"{self.name} - {self.get_role_display()}"



class Estudios(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_estudio')
      empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='empleados_estudio', blank=True, null=True)
      name = models.CharField(max_length=100, blank=False, null=False)
      description = models.TextField()
      img = models.ImageField(upload_to='media/estudios', null=True, blank=True, verbose_name='Imagen blanca')
      img_2 = models.ImageField(upload_to='media/estudios', null=True, blank=True, verbose_name='Imagen negra')
      background_img = models.ImageField(upload_to='media/estudios', null=True, blank=True, verbose_name='Imagen de fondo')
      date = models.DateTimeField(auto_now_add=True)

      is_active = models.BooleanField(default=False)

      
      class Meta:
            verbose_name = 'estudio'
            verbose_name_plural = 'estudios'
      
      def __str__(self):
            return self.name


class Service(models.Model):
      name = models.CharField(max_length=100, blank=False, null=False)
      description = models.TextField(blank=True, null=True)
      img = models.ImageField(upload_to='media/servicios', null=True)
      date = models.DateTimeField(auto_now_add=True)

      # Oferta de servicios, seran aplicados a todos los planes de este servicio
      # Si hay una oferta debe de haber un valor mayor a 0 en discount o mount
      
      is_offer = models.BooleanField(default=False)
      discount = models.IntegerField(default=0, blank=True, null=True)
      porcent_discount = models.IntegerField(default=0, blank=True, null=True)
      mount = models.IntegerField(default=0, blank=True, null=True)
      is_active = models.BooleanField(default=True)
      
      class Meta:
            verbose_name = 'servicio'
            verbose_name_plural = 'servicios'
      
      def __str__(self):
            return self.name


class Like(models.Model):
      plan = models.ForeignKey('Plan', on_delete=models.CASCADE, blank=True, null=True, related_name='likes')
      date = models.DateTimeField(auto_now_add=True)
      
      class Meta:
            verbose_name = 'like'
            verbose_name_plural = 'likes'
      
      def __str__(self):
            return self.plan.name

class Plan(models.Model):
      service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='planes')
      name = models.CharField(max_length=100, blank=False, null=False)
      description = models.TextField( blank=True, null=True)
      price = models.IntegerField(blank=False, null=False)
      img = models.ImageField(upload_to='media/planes', null=True, blank=True)
      img_back = models.ImageField(upload_to='media/planes', null=True, blank=True)
      date = models.DateTimeField(auto_now_add=True)
      is_active = models.BooleanField(default=True)
      
      time = models.TimeField(verbose_name="Hora de inicio", blank=True, null=True, default="08:00")

      # Oferta de planes
      is_offer = models.BooleanField(default=False)
      discount = models.IntegerField(default=0, blank=True, null=True)
      porcent_discount = models.IntegerField(default=0, blank=True, null=True)
      mount = models.IntegerField(default=0, blank=True, null=True)

      class Meta:
            verbose_name = 'plan'
            verbose_name_plural = 'planes'
      
      def __str__(self):
            return self.name





class Caracteristica(models.Model):
      plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True, related_name='caracteristicas')
      name = models.CharField(max_length=100, blank=False, null=False)
      date = models.DateTimeField(auto_now_add=True)
      
      class Meta:
            verbose_name = 'caracteristica'
            verbose_name_plural = 'caracteristicas'
      
      def __str__(self):
            return self.name


class Moment(models.Model):
      service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='momentos')
      name = models.CharField(max_length=100, blank=False, null=False)
      img = models.ImageField(upload_to='media/momentos', null=True)
      date = models.DateTimeField(auto_now_add=True)
      
      class Meta:
            verbose_name = 'momento'
            verbose_name_plural = 'momentos'
      
      def __str__(self):
            return self.name



class ImgMoment(models.Model):
      moment = models.ForeignKey(Moment, on_delete=models.CASCADE, blank=True, null=True, related_name='img_moments')
      img = models.ImageField(upload_to='media/imagenes', null=True, blank=True)
      date = models.DateTimeField(auto_now_add=True)
      
      class Meta:
            verbose_name = 'imagen'
            verbose_name_plural = 'imagenes'
      
      def __str__(self):
            return self.img.url
      

      




class Client(models.Model):
      name = models.CharField(max_length=100, blank=True, null=True)
      last_name = models.CharField(max_length=100, blank=True, null=True)
      email = models.EmailField(max_length=100, blank=True, null=True)
      phone = models.CharField(max_length=20, blank=True, null=True)
      date = models.DateTimeField(auto_now_add=True)
      
      class Meta:
            verbose_name = 'cliente'
            verbose_name_plural = 'clientes'
      
      def __str__(self):
            return self.name

# Las sales son las ventas que se realizan en el estudio, son equivalentes a las (citas)
# que se realizan en un estudio de fotografía, en este modelo se almacena la información
# de la venta, el cliente, el plan, los adicionales, el monto, el pago, las fechas de inicio
# y finalización, y el estado de la venta.
class Sale(models.Model):
#  Datos del usuario o cliente
      name_client = models.CharField(max_length=100, blank=True, null=True)
      email_client = models.EmailField(max_length=100, blank=True, null=True)
      phone_client = models.CharField(max_length=20, blank=True, null=True)
      phone_no_formate = models.CharField(max_length=20, blank=True, null=True)  # Teléfono sin formato para whatsapp
      descrition = models.TextField(blank=True, null=True) # Descripción para la venta
      is_cliente = models.BooleanField(default=False) # Si el cliente es nuevo
      client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_sale', null=True, blank=True)

      
# Datas de plan escogido
      pk_plan = models.IntegerField(default=0, blank=True, null=True)
      name_plan = models.CharField(max_length=100, blank=True, null=True)
      description_plan = models.TextField(blank=True, null=True)
      price_plan = models.IntegerField(blank=True, null=True)
      img = models.ImageField(upload_to='media/ventas', null=True, blank=True)
      date = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")
      is_active = models.BooleanField(default=True)

# Estado de la venta
      mount = models.IntegerField(blank=True, null=True, default=0) # Monto que abonado
      debit_mount = models.IntegerField(blank=True, null=True, default=0) # Monto que se debe restante
      is_reserve = models.BooleanField(default=False) # Reserva de la venta
      payment = models.BooleanField(blank=True, null=True) # Pago de la venta

# Procesos de fotografias
      start_proces_date = models.DateField(verbose_name="Fecha de inicio", blank=True, null=True)
      end_proces_date = models.DateField(verbose_name="Fecha final", blank=True, null=True)
      finalize = models.BooleanField(default=False) # Procesos de fotografias finalizado
      saled_date = models.DateField(verbose_name="Fecha de facturación", blank=True, null=True)  # Fecha de facturación

# Cuando se acordo la venta (cita)
      date_choice = models.DateField(verbose_name="Fecha seleccionada", blank=True, null=True) # Fecha de la cita
      HOUR_CHOICES = [(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(8, 18)]
      time = models.CharField(max_length=5, choices=HOUR_CHOICES, verbose_name="Hora seleccionada", blank=True, null=True, default="")

# Datos para la factura
      credit_fiscal = models.BooleanField(default=False) # Factura con crédito fiscal
      credito_fiscal = models.CharField(
            default='B01000000',
            max_length=255,
            blank=True,
            null=True,
            verbose_name="Creditos Fiscales"
      )
      cosumidor_final = models.CharField(
            default='B02000000',
            max_length=255,
            blank=True,
            null=True,
            verbose_name="Consumidor Final"
      )

      # Opciones para el tipo de venta
      SALE_TYPE_CHOICES = [
            ('credito', 'Crédito Fiscal'),
            ('consumidor', 'Consumidor Final'),
      ]

      sale_type = models.CharField(
            max_length=13,
            choices=SALE_TYPE_CHOICES,
            default='consumidor',  # Por defecto: Consumidor Final
            verbose_name="Tipo de Venta"
      )

      # RNC del cliente
      rnc_client = models.CharField(default='', max_length=255, blank=True, null=True)
      name_company_client = models.CharField(default='', max_length=255, blank=True, null=True)
      discount = models.BooleanField(default=True)  # Aplica para descuento

      # Asociar venta  aun contacto (cliente)
      contact = models.ForeignKey('Contact', on_delete=models.CASCADE, blank=True, null=True, 
                              related_name='sale_contact')

      def __str__(self):
            return f"Venta del {self.date.strftime('%d/%m/%Y')} - {self.name_client}"




class Adicional(models.Model):
      sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_adicionales')
      name = models.CharField(max_length=100, blank=False, null=False)
      description = models.TextField(blank=True, null=True)
      price = models.IntegerField(blank=False, null=False)
      date = models.DateTimeField(auto_now_add=True)
      
      class Meta:
            verbose_name = 'adicional'
            verbose_name_plural = 'adicionales'
      
      def __str__(self):
            return self.name



# Administrar Caja del estudio

class Box(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='box', null=True, blank=True)

# Estado de caja 
      open = models.BooleanField(default=True)
      date_opening = models.DateTimeField(auto_now_add=True)
      date_close = models.DateTimeField(null=True, blank=True)

      def __str__(self):
            return f" Caja {'abierta' if self.open else ' cerrada'} por {self.user.first_name} {self.user.last_name}"


# Movimientos de caja
class Movements(models.Model):
      TYPE_CHOICE = [
            ('ingreso', 'Ingreso'),
            ('gasto', 'Gasto'),

            # Moviemientos de cierre
            ('cierre', 'Cierre'),
            ('apertura', 'Apertura'),

            #  Movimientos de edición, creación, eliminación
            ('editar', 'Editar'),
            ('crear', 'Crear'),
            ('eliminar', 'Eliminar'),

            # Movimientos de ventas
            ('venta', 'Venta'),
            ('reserva', 'Reserva'),
            ('pago', 'Pago'),
            ('finalizar', 'Finalizar'),

      ]

      box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='movements', null=True, blank=True)
      type = models.CharField(max_length=15, choices=TYPE_CHOICE)
      mount = models.IntegerField(default=0, blank=False, null=False)
      description = models.TextField(default='Sin descripción', blank=True, null=True)
      date = models.DateTimeField(auto_now_add=True)

# Historial de movientos
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_move', null=True, blank=True)

      def __str__(self):
            return f"{self.type.capitalize()} de {'Efectuando caja' if self.mount else 'Movimiento'} el {self.date}"
      

class Config(models.Model):
      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='config', null=True, blank=True)
      mode = models.BooleanField(default=True) 
      # Si modo es True, el estudio esta en modo oscuro y si es False, el estudio esta en modo claro
      date = models.DateTimeField(auto_now_add=True)

      def __str__(self):
            return f"Configuración de {self.user.first_name} {self.user.last_name}"
      

class Facturacion(models.Model):
      estudio = models.ForeignKey(Estudios, on_delete=models.CASCADE, related_name='factura', null=True, blank=True)
      date = models.DateTimeField(auto_now_add=True)
      mount = models.IntegerField(default=0, blank=False, null=False)
      description = models.TextField(default='Sin descripción', blank=True, null=True)
      img = models.ImageField(upload_to='media/factura', null=True, blank=True)

      payment = models.BooleanField(default=False)
      last_payment_date = models.DateField(verbose_name="Fecha del último pago", blank=True, null=True)
      next_payment_date = models.DateField(verbose_name="Fecha del próximo pago", blank=True, null=True)


      def __str__(self):
            return f"Factura de {self.estudio.name} "
      

class Contact(models.Model):
      full_name = models.CharField(default='', max_length=25)
      phone = models.CharField(default='', max_length=15, blank=True)
      email = models.EmailField(max_length=100, blank=True, null=True)

      # Imagen de perfil
      img = models.ImageField(upload_to='media/contact', null=True, blank=True)
      date = models.DateField(default=timezone.now, verbose_name='Fecha de creacion')

      def __str__(self):
            return f'{self.full_name} - {self.phone} - {self.email}'