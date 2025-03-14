from  google import genai

from django.http import JsonResponse
from datetime import datetime
from . import models
from django.db.models import Q

def QuestionGemini(request):
      data = {'data': False}
      client = genai.Client(api_key="AIzaSyAlRiEbU6bhninS9aZvaO5MfB8jWyzfjw0")
      your_question  = request.GET.get('question')

      asisten_response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents=your_question,)
      print(asisten_response.text)

      if your_question:
            data = {
                  'your_question': your_question,
                  'asistent_response': asisten_response.text if asisten_response.text else 'No se encontró respuesta'
            }
      return JsonResponse(data)