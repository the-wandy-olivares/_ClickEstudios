from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Configuration, ModelsIA

class Asistente(TemplateView):
    template_name = 'asistente/asistente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['configuration'] = Configuration.objects.get(id=1)
        context['models_ia'] = ModelsIA.objects.filter(is_active= True)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        cf =  Configuration.objects.get(id=1)
        if request.POST.get('active-local') or 'None':
            if cf.is_local == True:
                cf.is_local = False
            else:
                cf.is_local = True
            cf.save()
        context['configuration'] = Configuration.objects.get(id=1)
        return self.render_to_response(context)