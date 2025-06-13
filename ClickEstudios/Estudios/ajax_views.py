from datetime import datetime
from django.http import JsonResponse
from . import models
from django.db.models import Q


def VerifyDateChoice(request):
      date = request.GET.get('date_choice')
      if date:
            try:
                  date = datetime.strptime(date, '%Y-%m-%d').date()
                  sales = models.Sale.objects.filter(date_choice=date)
                  if sales.exists():
                        selected_hours = [int(sale.time.split(':')[0]) for sale in sales] 
                         # Si `time` es un string tipo "HH:MM:SS"
                        available_hours = [f"{hour:02d}:00" for hour in range(8, 18) if hour not in selected_hours]
                        context = {
                              'true': False,
                              'available_hours': available_hours
                        }
                        return JsonResponse(context, safe=False)
            except ValueError:
                  return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

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
            # Búsqueda general si no se especifica 'cita', 'cliente' o número de teléfono
            data = models.Sale.objects.filter(
                        Q(name_client__icontains=search_term) | 
                        Q(email_client__icontains=search_term) | 
                        Q(phone_no_formate__icontains=search_term),
                        is_reserve=True,
                        finalize=False
            ).values('id', 'name_client', 'email_client', 'phone_no_formate')
      return JsonResponse(list(data), safe=False)



def GetEstudios(request):
    data = {'data': False}
    if models.Estudios.objects.filter(name='ClickEstudios').exists():
        estudio = models.Estudios.objects.get(name='ClickEstudios')
        data = {
            'id': estudio.id,
            'name': estudio.name,
            'description': estudio.description,  # Agrega los campos que necesites
            'img': estudio.img.url if estudio.img else None,
            'img2': estudio.img_2.url if estudio.img_2 else None
        }
    return JsonResponse(data)



def SearchMove(request):
      d = request.GET.get('search', '').strip()
      data = []
      if d:
            data = models.Movements.objects.filter(description__icontains=d).values('id', 'description', 'description', 'date', 'mount', 'type')
      return JsonResponse(list(data), safe=False)


def SearchCitas(request):
      d = request.GET.get('search', '').strip()
      data = []
      if d:
            data = models.Sale.objects.filter(name_client__icontains=d).values('id', 'name_client', 'email_client', 'phone_client', 'descrition', 'name_plan', 'price_plan', 'img', 'time', 'date_choice', 'is_reserve', 'mount', 'debit_mount', 'payment', 'finalize')
      return JsonResponse(list(data), safe=False)