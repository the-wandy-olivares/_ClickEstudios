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