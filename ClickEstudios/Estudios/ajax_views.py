from datetime import datetime
from django.http import JsonResponse
from . import models

def VerifyDateChoice(request):
      date = request.GET.get('date_choice')
      print("Hello", date)  # Para depuración
      if date:
            try:
                  date = datetime.strptime(date, '%Y-%m-%d').date()
                  sales = models.Sale.objects.filter(date_choice=date)
                  if sales.exists():
                        # Convertimos la hora de cadena a un entero
                        selected_hours = [int(sale.time.split(':')[0]) for sale in sales]  # Si `time` es un string tipo "HH:MM:SS"
                        print(selected_hours)
                        available_hours = [f"{hour:02d}:00" for hour in range(8, 18) if hour not in selected_hours]
                        context = {
                              'true': False,
                              'available_hours': available_hours
                        }
                        return JsonResponse(context, safe=False)
            except ValueError:
                  return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

      # Si no se pasa una fecha o no hay ventas en la fecha seleccionada
      available_hours = [f"{hour:02d}:00" for hour in range(8, 18)]
      context = {
            'true': True,
            'available_hours': available_hours
      }
      return JsonResponse(context, safe=False)




def Search(request):
      d = request.GET.get('search', '').strip()
      data = []
    
      if d:
            search_term = d.lower()
            if search_term in ['citas', 'cliente']:
                  search_term = ''  # Eliminar la palabra 'cita' o 'cliente' del término de búsqueda
            if 'citas' in d.lower():
                  data = models.Sale.objects.filter(is_reserve=True, finalize=False,  name_client__icontains=search_term).values('id', 'name_client')
            elif 'cliente' in d.lower():
                  data = models.Sale.objects.filter(is_reserve=False, finalize=False, name_client__icontains=search_term).values('id', 'name_client')
            else:
                  # Búsqueda general si no se especifica 'cita' o 'cliente'
                  data = models.Sale.objects.filter(name_client__icontains=search_term).values('id', 'name_client')

      return JsonResponse(list(data), safe=False)



def GetEstudios(request):
    data = None
    if models.Estudios.objects.filter(name='ClickEstudios').exists():
        estudio = models.Estudios.objects.get(name='ClickEstudios')
        data = {
            'id': estudio.id,
            'name': estudio.name,
            'description': estudio.description,  # Agrega los campos que necesites
            'img': estudio.img.url if estudio.img else None,
            'img2': estudio.img2.url if estudio.img2 else None
        }

    return JsonResponse(data)