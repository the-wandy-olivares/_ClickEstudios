from  google import genai

from django.http import JsonResponse
from datetime import datetime
from . import models
from django.db.models import Q
from Estudios.models import Sale, Movements, Service, Plan, Caracteristica




def Gastos():
      movimientos = Movements.objects.all()
      gastos = 0
      for movimiento in movimientos:
            if movimiento.type == 'egreso':
                  gastos += movimiento.mount

      return gastos

def Obtener_Total_Ingresos():
      movimientos = Movements.objects.all()
      ingresos = 0
      for movimiento in movimientos:
            if movimiento.type == 'ingreso':
                  ingresos += movimiento.mount
      return 



def CleanQuestion(question):
      if 'vent'  in question.lower():
            sale = Sale.objects.all().order_by('-id')[:50]
            sales_data = []
            for s in sale:
                  sales_data.append({
                        'name_plan': s.name_plan if s.name_plan else 'N/A',
                        'payment': s.payment if 'Si' else 'No',
                        'name_client': s.name_client if s.name_client else 'N/A',
                        'email_client': s.email_client if s.email_client else 'N/A',
                        'phone_client': s.phone_client if s.phone_client else 'N/A',
                        'dia_de_la_cita': s.date_choice,
                        'monto_faltante': f"{s.debit_mount:,}",
                        'monto_pagado': f"{s.mount:,}",
                  })
            return f'{sales_data}'
      
      elif 'citas' in question.lower():
            citas = Sale.objects.filter(is_reserve=True, finalize=False).order_by('-id')[:50]
            citas_data = []
            for s in citas:
                  citas_data.append({
                        'name_plan': s.name_plan if s.name_plan else 'N/A',
                        'payment': s.payment if 'Si' else 'No',
                        'name_client': s.name_client if s.name_client else 'N/A',
                        'email_client': s.email_client if s.email_client else 'N/A',
                        'phone_client': s.phone_client if s.phone_client else 'N/A',
                        'dia_de_la_cita': s.date_choice,
                        'monto_faltante': f"{s.debit_mount:,}",
                        'monto_pagado': f"{s.mount:,}",
                  })
            return citas_data 
      
      elif 'plan' in question.lower() :
            plan_data = []
            plan = Plan.objects.all().order_by('-id')[:30]
            for p in plan:
                  plan_data.append({
                        'servicio_asociado': p.service.name if p.service and p.service.name else 'N/A',
                        'name_plan': p.name if p.name else 'N/A',
                        'price_plan': f"{p.price:,}",
                        'caracteristicas': [c.name for c in p.caracteristicas.all()],
                  })
            return f'{plan_data}'
      
      elif 'serv' in question.lower() :
            service_data = []
            service = Service.objects.all().order_by('-id')[:25]
            for s in service:
                  service_data.append({
                        'name': s.name if s.name else 'N/A',
                  })
            return f'{service_data}'

      else:
            return False
      
      

def QuestionGemini(request):
      your_question  = request.GET.get('question')
      data = {'data': False}
      if your_question:
            client = genai.Client(api_key="AIzaSyAlRiEbU6bhninS9aZvaO5MfB8jWyzfjw0")
            if CleanQuestion(your_question)  != False:
                  question =   CleanQuestion(your_question) 
            else:
                  question = your_question
            
            # asisten_response = CleanQuestion(your_question)
            # print(CleanQuestion(your_question))

            asisten_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents = f"""
                  Sistema: ClickEstudios
                  Contexto: Click, Asistente de un estudio y das respuestas puntuales.
                  Objetivo: Proporcionar información detallada sobre planes, servicios, ventas, citas comparaciones y de mas.
                  Fecha de hoy: {datetime.now().strftime('%d/%m/%Y')}
                  Pregunta:  {question}
                  """,)
            
            if your_question:
                  data = {
                        'your_question': your_question,
                        'asistent_response': asisten_response.text if asisten_response.text else 'No se encontró respuesta'
                  }
      return JsonResponse(data)