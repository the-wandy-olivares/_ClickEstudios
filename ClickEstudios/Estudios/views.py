from django.shortcuts import render, redirect   
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models, forms


class Dashboard(TemplateView):
    def get(self, request):
        return render(request, 'estudios/dashboard.html')


class Pos(TemplateView):
    template_name = 'pos/pos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_choices'] = models.Service.objects.all()
        context['plan_choices'] = models.Plan.objects.all()
        context['sales'] = models.Sale.objects.all()
        return context

class Service(TemplateView):
        template_name = 'service/service.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['services'] = models.Service.objects.all()
            return context

class ServiceDetail(DetailView):
        model = models.Service
        template_name = 'service/service-detail.html'
        context_object_name = 'service'


        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['plans'] = models.Plan.objects.filter(service=self.object)
                return context


class ServiceCreate(CreateView):
        model = models.Service
        form_class = forms.Service
        template_name = 'service/service-create.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context


        def form_valid(self, form):
            # Guarda el objeto y redirige al éxito
            self.object = form.save()
            return redirect(self.get_success_url())

        def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))


        def get_success_url(self):
            # Retorna la URL a la que redirigirá después de un submit exitoso
            return reverse_lazy('estudios:service')


class ServiceUpdate(UpdateView):
    model = models.Service
    form_class = forms.Service
    template_name = 'service/service-update.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

    def form_valid(self, form):
                # Guarda el objeto y redirige al éxito
            self.object = form.save()
            return redirect(self.get_success_url())

    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
            # Retorna la URL a la que redirigirá después de un submit exitoso
            return reverse_lazy('estudios:service')



class ServiceDelete(DeleteView):
    model = models.Service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:service')


# Plans
class Plan(TemplateView):
    template_name = 'plan/plan.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = models.Plan.objects.all()
        return context


class PlanDetail(DetailView):
    model = models.Plan
    template_name = 'plan/plan-detail.html'
    context_object_name = 'plan'


class PlanCreate(CreateView):
    model = models.Plan
    form_class = forms.Plan
    template_name = 'plan/plan-create.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Guarda el objeto y redirige al éxito
        self.object = form.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:plan')



class PlanUpdate(UpdateView):
        model = models.Plan
        form_class = forms.Plan
        template_name = 'plan/plan-update.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context


        def form_valid(self, form):
                    # Guarda el objeto y redirige al éxito
                print(form)
                self.object = form.save()
                return redirect(self.get_success_url())

        def form_invalid(self, form):
            print(form.errors)
            return self.render_to_response(self.get_context_data(form=form))

        def get_success_url(self):
            # Retorna la URL a la que redirigirá después de un submit exitoso
            return reverse_lazy('estudios:plan')


class PlanDelete(DeleteView):
    model = models.Plan

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:plan')



class Sale(TemplateView):
    template_name = 'sale/sale.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales'] = models.Sale.objects.all()
        return context


class SaleDetail(DetailView):
    model = models.Sale
    template_name = 'sale/sale-detail.html'
    context_object_name = 'sale'


class SaleCreate(CreateView):
    model = models.Sale
    form_class = forms.Sale
    template_name = 'sale/sale-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        plan_id = self.kwargs.get('pk')
        if plan_id:
            plan = models.Plan.objects.get(pk=plan_id)
            form.instance.name_plan = plan.name
            form.instance.description_plan = plan.description
            form.instance.price_plan = plan.price

        # Guarda el objeto y redirige al éxito
        self.object = form.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:pos')


class SaleUpdate(UpdateView):
    model = models.Sale
    form_class = forms.Sale
    template_name = 'sale/sale-update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Guarda el objeto y redirige al éxito
        self.object = form.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:sale')