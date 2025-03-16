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
                        'venta_registrada': s.date,
                        'monto_faltante': f"{s.debit_mount:,}",
                        'monto_pagado': f"{s.mount:,}",
                  })
            return f'{sales_data}'
      
      elif 'cita'  in question.lower():
            citas = Sale.objects.filter(is_reserve=True, finalize=False).order_by('-id')[:50]
            citas_data = []
            for s in citas:
                  citas_data.append({
                        'name_plan': s.name_plan if s.name_plan else 'N/A',
                        'payment': s.payment if 'Si' else 'No',
                        'name_client': s.name_client if s.name_client else 'N/A',
                        'email_client': s.email_client if s.email_client else 'N/A',
                        'phone_client': s.phone_client if s.phone_client else 'N/A',
                        'fecha_de_la_cita': s.date_choice,
                        'hora_de_la_cita': s.time,
                        'monto_faltante': f"{s.debit_mount:,}",
                        'monto_pagado': f"{s.mount:,}",
                  })
            return citas_data if citas_data else 'No hay citas pendientes'
      
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
            return plan_data if plan_data else 'No encuentro ese plan en mi lista'
      
      elif 'serv' in question.lower() :
            service_data = []
            service = Service.objects.all().order_by('-id')[:25]
            for s in service:
                  service_data.append({
                        'name': s.name if s.name else 'N/A',
                  })
            return service_data if service_data else 'No encuentro ese servicio en mi lista'

      else:
            return 'Solo puedo responder preguntas sobre ventas, citas, planes y servicios'
      
      

def QuestionGemini(request):
      your_question  = request.GET.get('question')
      data = {'data': False}
      if your_question:
            client = genai.Client(api_key="AIzaSyAlRiEbU6bhninS9aZvaO5MfB8jWyzfjw0")
            asisten_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents = f"""
                    Sistema: ClickEstudios
                    Contexto: ClickEstudios es un asistente virtual para la gestión de un estudio fotográfico, proporcionando respuestas precisas y detalladas.
                    Objetivo: Proporcionar información específica y actualizada sobre planes, servicios, ventas, citas y otros aspectos relacionados con la gestión del estudio.
                    Fecha actual: {datetime.now().strftime('%d/%m/%Y')}
                    Pregunta del usuario: {your_question}
                    Información adicional: {CleanQuestion(your_question)}
                    """,)
            
            if your_question:
                  data = {
                        'your_question': your_question,
                        'asistent_response': asisten_response.text if asisten_response.text else 'No se encontró respuesta'
                  }
      return JsonResponse(data)