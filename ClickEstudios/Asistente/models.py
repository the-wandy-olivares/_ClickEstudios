from django.db import models

# Create your models here.
class Configuration(models.Model):
      AI_CHOICES = [
            ('gemini', 'Géminis'),
            ('chatgpt', 'Chat-GPT'),
            ('llama', 'Llama'),
            ('gemma', 'Gemma')
      ]

      model = models.CharField(max_length=10, choices=AI_CHOICES, default='gemini')
      is_local = models.BooleanField(default=False)

      
      def __str__(self):
            return f"Configuración: {self.get_model_display()}"
      


class ModelsIA(models.Model):
      name = models.CharField(max_length=90, default='local', blank=True, null=True)
      api_keys = models.TextField(default='', blank=True, null=True)

      is_active = models.BooleanField(default=False)

      
      def __str__(self):
            return f"{self.name} - {self.is_active}"
      



