from django.db import models
from django.contrib.auth.models import User





class Empleado(models.Model):
      ROLE_CHOICES = [
            ('admin', 'Administrador'),
            ('supervisor', 'Supervisor'),
            ('customer_service', 'Servicio al Cliente'),
            ('photographer', 'Fotografo'),
            ('editor', 'Editor'),
            ('estandard', 'Estandar'),
      ]

      estudio = models.ForeignKey('Estudios', on_delete=models.CASCADE, related_name='empleados')
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
      empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='empleados_estudio')
      name = models.CharField(max_length=100, blank=False, null=False)
      description = models.TextField()
      img = models.ImageField(upload_to='media/estudios', null=True, blank=True)
      date = models.DateTimeField(auto_now_add=True)

      
      class Meta:
            verbose_name = 'estudio'
            verbose_name_plural = 'estudios'
      
      def __str__(self):
            return self.name


class Service(models.Model):
      name = models.CharField(max_length=100, blank=False, null=False)
      description = models.TextField(blank=True, null=True)
      img = models.ImageField(upload_to='media/servicios', null=True, blank=True)
      date = models.DateTimeField(auto_now_add=True)

      is_active = models.BooleanField(default=True)
      class Meta:
            verbose_name = 'servicio'
            verbose_name_plural = 'servicios'
      
      def __str__(self):
            return self.name


class Plan(models.Model):
      service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='planes')
      name = models.CharField(max_length=100, blank=False, null=False)
      description = models.TextField( blank=True, null=True)
      price = models.IntegerField(blank=False, null=False)
      img = models.ImageField(upload_to='media/planes', null=True, blank=True)
      img_back = models.ImageField(upload_to='media/planes', null=True, blank=True)
      date = models.DateTimeField(auto_now_add=True)
      is_active = models.BooleanField(default=True)
      
      class Meta:
            verbose_name = 'plan'
            verbose_name_plural = 'planes'
      
      def __str__(self):
            return self.name



class Moment(models.Model):
      service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='momentos')
      name = models.CharField(max_length=100, blank=False, null=False)
      img = models.ImageField(upload_to='media/momentos', null=True, blank=True)
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