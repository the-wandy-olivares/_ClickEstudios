from django.urls import path
from . import views, views_ajax

app_name = 'asistente'
urlpatterns = [
      path('', views.Asistente.as_view(), 
            name='asistente'),


# Views Ajax
      path('ajax/question-gemini/', views_ajax.QuestionGemini,
            name='question_gemini'),

]