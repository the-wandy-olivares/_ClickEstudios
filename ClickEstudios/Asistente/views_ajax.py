from .models import Configuration
from .mixing import IA

def Asistente(request):
      ia = Configuration.objects.get(id=1)
      if ia.is_local == True:
            return  IA.Gemma(request) 
      else:
            return  IA.Gemini(request) 