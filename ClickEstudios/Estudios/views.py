import json
import random
from django.shortcuts import render, redirect   
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models, forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Utilidades
from . import utils
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# Cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.contrib import messages


from django.shortcuts import render


def Status404(request, exception):
    return render(request, 'component/404.html', status=404)



class OfertaService(TemplateView):
    template_name = 'oferta/oferta-service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = models.Service.objects.all()
        return context

class Dashboard(TemplateView):
    template_name = 'dashboard/dashboard.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales'] = models.Sale.objects.all()
        context['en'] = models.Sale.objects.filter(date__month=1).count() 
        context['fe'] = models.Sale.objects.filter(date__month=2).count()
        context['ma'] = models.Sale.objects.filter(date__month=3).count()
        context['ab'] = models.Sale.objects.filter(date__month=4).count()
        context['my'] = models.Sale.objects.filter(date__month=5).count()
        context['ju'] = models.Sale.objects.filter(date__month=6).count()
        context['jul'] = models.Sale.objects.filter(date__month=7).count()
        context['ag'] = models.Sale.objects.filter(date__month=8).count()
        context['set'] = models.Sale.objects.filter(date__month=9).count()
        context['oc'] = models.Sale.objects.filter(date__month=10).count()
        context['nov'] = models.Sale.objects.filter(date__month=11).count()
        context['dic'] = models.Sale.objects.filter(date__month=12).count()
        return context




class Pos(TemplateView):
    template_name = 'pos/pos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_open_box = models.Box.objects.filter(open=True).last()
        if last_open_box:
            if last_open_box.created_box:
                if last_open_box.created_box.date() != timezone.now().date():
                    context['ask_due_box'] = True
                    context['created_box'] = last_open_box.created_box.date()
                    context['timemezone'] = timezone.now().date()

        context['service_choices'] = models.Service.objects.all()
        context['plan_choices'] = models.Plan.objects.all()
        context['sales'] = models.Sale.objects.filter(is_reserve=False,
                            finalize=False).order_by('-id')
        context['box_is_open'] = models.Box.objects.filter(open=True).exists() 
        context['today'] = timezone.now().date()
        context['time_now'] =  timezone.localtime(timezone.now(), timezone.get_current_timezone()).astimezone(timezone.get_fixed_timezone(-240)).replace(minute=0, second=0, microsecond=0).strftime('%H:%M')
        return context
    
    def filter_sales(self, filter_option):
        today = timezone.localtime().date()  # Fecha actual en la zona horaria local    
        TIME_NOW = timezone.localtime(timezone.now(), timezone.get_current_timezone()).astimezone(timezone.get_fixed_timezone(-240)).replace(minute=0, second=0, microsecond=0).strftime('%H:%M')
        filters = {
            'today': models.Sale.objects.filter(date_choice=today),
            'hour': models.Sale.objects.filter(date_choice=today, time__gte=TIME_NOW),
            'past_hour': models.Sale.objects.filter(date_choice=today, time__lt=TIME_NOW),
            'past': models.Sale.objects.filter(date_choice__lt=today),
            'future': models.Sale.objects.filter(date_choice__gt=today),
            'all': models.Sale.objects.all(),
        }
        # Filtrar por reservas activas y no finalizadas
        sales_query = filters.get(filter_option, filters['hour']).filter(is_reserve=True, finalize=False)
        return sales_query.order_by('-date_choice', 'time')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        filter_option = request.GET.get('filter', 'all')  # Si no se especifica, usa 'hour'
        context['sales_reservers'] = self.filter_sales(filter_option)
        context['filter_option'] = filter_option
        return self.render_to_response(context)



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
                context['moments'] = models.Moment.objects.filter(service=self.object)
                return context


class ServiceClientSelect(DetailView):
        model = models.Service
        template_name = 'service/service-client-select.html'
        context_object_name = 'service'


        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['plans'] = models.Plan.objects.filter(service=self.object)
                context['moments'] = models.Moment.objects.filter(service=self.object)
                return context



class ServiceCreate(CreateView):
        model = models.Service
        form_class = forms.Service
        template_name = 'service/service-create.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context


        def form_valid(self, form):
            img = form.instance.img
            img_temporary = Image.open(img)

            # Resize image to 720p

            if img_temporary.mode == 'RGBA':
                img_temporary = img_temporary.convert('RGB')
            output_io_stream = BytesIO()
            img_temporary.save(output_io_stream, format='JPEG', quality=65)
            output_io_stream.seek(0)
            form.instance.img = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.jpg" % img.name.split('.')[0], 'image/jpeg', output_io_stream.getbuffer().nbytes, None)


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
            img = form.instance.img
            img_temporary = Image.open(img)

            # Resize image to 720p
            # Resize image to 720p

            if img_temporary.mode == 'RGBA':
                img_temporary = img_temporary.convert('RGB')
            output_io_stream = BytesIO()
            img_temporary.save(output_io_stream, format='JPEG', quality=65)
            output_io_stream.seek(0)
            form.instance.img = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.jpg" % img.name.split('.')[0], 'image/jpeg', output_io_stream.getbuffer().nbytes, None)

                # Guarda el objeto y redirige al éxito
            self.object = form.save()
            return redirect(self.get_success_url())

    def form_invalid(self, form):
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
            # Retorna la URL a la que redirigirá después de un submit exitoso
            return reverse_lazy('estudios:service')



class ServiceDelete(DeleteView):
    template_name = 'service/delete.html'
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
        context['services'] = models.Service.objects.all()
        return context


class PlanDetail(DetailView):
    model = models.Plan
    template_name = 'plan/plan-detail.html'
    context_object_name = 'plan'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caracteristicas'] = models.Caracteristica.objects.filter(plan=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('name'):
            caract = models.Caracteristica(
                plan=models.Plan.objects.get(pk=self.kwargs.get('pk')),
                name=request.POST.get('name'),
            )
            caract.save()
        if request.POST.get('delete'):
            caract = models.Caracteristica.objects.get(pk=request.POST.get('delete'))
            caract.delete()
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:plan-detail', kwargs={'pk': self.kwargs.get('pk')})


class PlanCreate(CreateView):
    model = models.Plan
    form_class = forms.Plan
    template_name = 'plan/plan-create.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        img = form.instance.img
        img_temporary = Image.open(img)
        
        # Resize image to 720p

        if img_temporary.mode == 'RGBA':
            img_temporary = img_temporary.convert('RGB')
        output_io_stream = BytesIO()
        img_temporary.save(output_io_stream, format='JPEG', quality=50)
        output_io_stream.seek(0)
        form.instance.img = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.jpg" % img.name.split('.')[0], 'image/jpeg', output_io_stream.getbuffer().nbytes, None)

        # Resize image to 140p for img_back
        img_temporary = img_temporary.resize((256, 140), Image.LANCZOS)
        if img_temporary.mode == 'RGBA':
            img_temporary = img_temporary.convert('RGB')
        output_io_stream = BytesIO()
        img_temporary.save(output_io_stream, format='JPEG', quality=35)
        output_io_stream.seek(0)
        form.instance.img_back = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s_back.jpg" % img.name.split('.')[0], 'image/jpeg', output_io_stream.getbuffer().nbytes, None)


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
            img = form.instance.img
            img_temporary = Image.open(img)
            
            # Resize image to 720p

            if img_temporary.mode == 'RGBA':
                img_temporary = img_temporary.convert('RGB')
            output_io_stream = BytesIO()
            img_temporary.save(output_io_stream, format='JPEG', quality=50)
            output_io_stream.seek(0)
            form.instance.img = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.jpg" % img.name.split('.')[0], 'image/jpeg', output_io_stream.getbuffer().nbytes, None)

            # Resize image to 140p for img_back
            img_temporary = img_temporary.resize((256, 140), Image.LANCZOS)
            if img_temporary.mode == 'RGBA':
                img_temporary = img_temporary.convert('RGB')
            output_io_stream = BytesIO()
            img_temporary.save(output_io_stream, format='JPEG', quality=35)
            output_io_stream.seek(0)
            form.instance.img_back = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s_back.jpg" % img.name.split('.')[0], 'image/jpeg', output_io_stream.getbuffer().nbytes, None)


            # Guarda el objeto y redirige al éxito
            self.object = form.save()
            return redirect(self.get_success_url())
        def form_invalid(self, form):
            print(form.errors)
            return self.render_to_response(self.get_context_data(form=form))

        def get_success_url(self):
            # Retorna la URL a la que redirigirá después de un submit exitoso
            return reverse_lazy('estudios:plan')


class PlanDelete(DeleteView):
    template_name = 'plan/plan-delete.html'
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


class SaleReserver(TemplateView):
    model = models.Sale
    form_class = forms.Sale
    template_name = 'sale/sale-reserver.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))
        context['sale'] = sale
        context['restante'] = sale.price_plan - sale.debit_mount
        return context
    

    def post(self, request, *args, **kwargs):
        new_mount = request.POST.get('mount')
        if new_mount:
            sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))

            # Reservar la venta
            sale.is_reserve = True
            new_mount = int(new_mount)
            sale.mount = (sale.mount or 0) + int(new_mount)

            sale.debit_mount -= new_mount
            if sale.mount >= sale.price_plan:
                sale.mount = sale.price_plan
                sale.payment = True
                description = 'Pago completado' + ' ' + sale.name_client + '-' + sale.name_plan +  ' ( Restante: ' + f"${sale.debit_mount:,}" + ')'
                sale.saled_date = timezone.now() # Fecha en la que se completo la venta
            else:
                description = 'Abono, ' + sale.name_client + ', ' + sale.name_plan + ' ( Restante: ' + f"${sale.debit_mount:,}" + ')'
                    # Restar monto 

            models.Movements.objects.create(
                user=request.user,
                box=models.Box.objects.get(open=True),
                mount= new_mount,
                type='ingreso',
                description=description
            )
            sale.save()


            return redirect('estudios:pos')
        return self.render_to_response(self.get_context_data())


class SaleCreate(CreateView):
    model = models.Sale
    form_class = forms.Sale
    template_name = 'sale/sale-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan'] =  models.Plan.objects.get(pk= self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        plan_id = self.kwargs.get('pk')
        if plan_id:
            plan = models.Plan.objects.get(pk=plan_id)
            form.instance.pk_plan = plan_id
            form.instance.name_plan = plan.name

            if plan.is_offer:
                    form.instance.debit_mount = plan.mount
            else:
                form.instance.debit_mount = plan.price

            form.instance.img = plan.img
            form.instance.description_plan = plan.description

            if plan.is_offer:
                    form.instance.price_plan = plan.mount
            else:
                    form.instance.price_plan = plan.price

            form.instance.finaliz = True
            form.instance.payment = True
            form.instance.is_reserve = True
            form.instance.phone_no_formate = form.instance.phone_client.replace('(', '').replace(')', '').replace(' ', '').replace('-', '') if form.instance.phone_client else None
            form.instance.saled_date = timezone.now()

        # Guarda el objeto y redirige al éxito
            models.Movements.objects.create(
                user=self.request.user,
                box=models.Box.objects.get(open=True),
                mount= form.instance.price_plan,
                type='ingreso',
                description=  'Pago completado' + ' ' + form.instance.name_client + '-' + plan.name
            )
        self.object = form.save()
        return redirect(self.get_success_url(self.object))

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self, sale):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:estudios' , kwargs={'pk': sale.pk})


class SaleUpdate(UpdateView):
    model = models.Sale
    form_class = forms.Sale
    template_name = 'sale/sale-update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plan'] = models.Plan.objects.filter(pk=self.object.pk_plan).last()
        return context

    def form_valid(self, form):
        # Guarda el objeto y redirige al éxito
        plan = models.Plan.objects.filter(pk=self.object.pk_plan).last()
        form.instance.name_plan = plan.name
        form.instance.debit_mount = plan.price
        form.instance.img = plan.img
        form.instance.description_plan = plan.description
        form.instance.price_plan = plan.price
        form.instance.phone_no_formate = form.instance.phone_client.replace('(', '').replace(')', '').replace(' ', '').replace('-', '') if form.instance.phone_client else None
        self.object = form.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:pos')
    

class SaleDelete(DeleteView):
    model = models.Sale
    template_name = 'sale/sale-delete.html'

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:pos')


class SaleCreateDateChoice(CreateView):
        model = models.Sale
        form_class = forms.Sale
        template_name = 'sale/sale-create-date-choice.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['plan'] = models.Plan.objects.get(pk=self.kwargs.get('pk'))
            return context

        def form_valid(self, form):
            plan_id = self.kwargs.get('pk')
            if plan_id:
                plan = models.Plan.objects.get(pk=plan_id)
                form.instance.pk_plan = plan_id
                form.instance.name_plan = plan.name

                if plan.is_offer:
                    form.instance.debit_mount = plan.mount
                else:
                    form.instance.debit_mount = plan.price

                form.instance.img = plan.img
                form.instance.description_plan = plan.description
                if plan.is_offer:
                    form.instance.price_plan = plan.mount
                else:
                    form.instance.price_plan = plan.price
                form.instance.phone_no_formate = form.instance.phone_client.replace('(', '').replace(')', '').replace(' ', '').replace('-', '') if form.instance.phone_client else None

                if form.instance.email_client:
                    utils.Send_Mail(form.instance.email_client, form.instance.name_client, plan.name, form.instance.date_choice, form.instance.time)
                    
                # Guarda el objeto y redirige al éxito
                self.object = form.save()



            return redirect(self.get_success_url())

        def form_invalid(self, form):
            print(form.errors)
            return self.render_to_response(self.get_context_data(form=form))

        def get_success_url(self):
            # Retorna la URL a la que redirigirá después de un submit exitoso
            return reverse_lazy('estudios:pos')

    


# Cliente adquiriendo venta

class SaleClientDateChoice(CreateView):
        model = models.Sale
        form_class = forms.Sale
        template_name = 'sale/sale-client-date-choice.html'
                
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['plan'] = models.Plan.objects.get(pk=self.kwargs.get('pk'))
            return context

        def form_valid(self, form):
            plan_id = self.kwargs.get('pk')
            if plan_id:
                plan = models.Plan.objects.get(pk=plan_id)
                form.instance.name_plan = plan.name
                if plan.is_offer:
                    form.instance.debit_mount = plan.mount
                else:
                    form.instance.debit_mount = plan.price
                form.instance.img = plan.img
                form.instance.description_plan = plan.description
                if plan.is_offer:
                        form.instance.price_plan = plan.mount
                else:
                        form.instance.price_plan = plan.price
                form.instance.phone_no_formate = form.instance.phone_client.replace('(', '').replace(')', '').replace(' ', '').replace('-', '') if form.instance.phone_client else None

                if form.instance.email_client:
                    utils.Send_Mail(form.instance.email_client, form.instance.name_client, plan.name, form.instance.date_choice, form.instance.time)
                    
                # Guarda el objeto y redirige al éxito
                self.object = form.save()



            return redirect(self.get_success_url())

        def form_invalid(self, form):
            print(form.errors)
            return self.render_to_response(self.get_context_data(form=form))
        

        def get_success_url(self):
            # Retorna la URL a la que redirigirá después de un submit exitoso
            return reverse_lazy('estudios:yes')


class Yes(TemplateView):
    template_name = 'yes/yes.html'


class Estudios(TemplateView):
    template_name = 'estudios/estudios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))
        sale_itebis = sale.price_plan * 0.18
        total = sale.price_plan 
        if sale.sale_adicionales.all():
            for adicional in sale.sale_adicionales.all():
                total += adicional.price

        total_itebis = total * 0.18
        context['total_itebis'] = total_itebis
        context['sale'] = sale
        if sale.discount:
            context['total_con_i'] = total 
        else:
            context['total_con_i'] = total + total_itebis

        context['estudios'] =  models.Estudios.objects.filter(name='ClickEstudios').exists() if models.Estudios.objects.get(name='ClickEstudios') else ''
    
        if models.Plan.objects.filter(id=sale.pk_plan).exists() == True:
            context['plan'] = models.Plan.objects.get(id=sale.pk_plan)

        context['total_sin'] = total
        context['total'] = total + total_itebis
        context['total_adicionales'] = total - sale.price_plan
        context['adicionales'] = sale.sale_adicionales.all()
        context['sale_itebis'] = sale_itebis
        context['sale_price_unitario'] = sale.price_plan + sale_itebis
        context['ncf'] =utils.GetNCF(sale.sale_type)
        return context


    def post(self, request, *args, **kwargs):

        if request.POST.get('search_rnc'):
            sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))
            sale.rnc_client = request.POST.get('search_rnc')
            sale.name_company_client = request.POST.get('search_name')
            sale.save()

        # Agregar adicional
        if request.POST.get('name'):
            sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))
            price = request.POST.get('price').replace(',', '')
            a = models.Adicional(
                    sale=sale,
                    name= request.POST.get('name'),
                    description= request.POST.get('description'),
                    price= int(price)
            )
            a.save()


        sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))
        if request.POST.get('discount') == 'on':
            if sale.discount:
                sale.discount = False
            else:
                sale.discount = True
            sale.save()

        

        if request.POST.get('invoice_type'):
            sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))
            sale.sale_type = request.POST.get('invoice_type')
            sale.discount = False
            sale.save()
        # Eliminar adicional
        if request.POST.get('delete'):
                adicional = models.Adicional.objects.get(pk=request.POST.get('delete'))
                adicional.delete()
        
        # Finalizar venta
        if request.POST.get('end'):

            sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))

            total = sale.price_plan 
            if sale.sale_adicionales.all():
                for adicional in sale.sale_adicionales.all():
                    total += adicional.price
            total_itebis = total * 0.18

            if sale.sale_type == 'credito':
                sale.credito_fiscal = utils.GetNCF('credito')
            else:
                sale.cosumidor_final = utils.GetNCF('consumidor')
            sale.finalize = True
            if sale.discount == False:
                models.Movements.objects.create(
                    user=self.request.user,
                    box=models.Box.objects.get(open=True),
                    mount= total_itebis,
                    type='ingreso',
                    description=  'Itbis: ' + ' ' + sale.name_client if sale.name_client else "Itbis en " + sale.name_plan
                )

            if sale.sale_adicionales.all():
                for adicional in sale.sale_adicionales.all():
                    models.Movements(
                        user=request.user,
                        box=models.Box.objects.get(open=True),
                        mount=adicional.price,
                        type='ingreso',
                        description=adicional.name + ' ' + adicional.description
                    ).save()
                    


            sale.save()
            return redirect('estudios:pos')
            
        return self.render_to_response(self.get_context_data())
    
@method_decorator(cache_page(3 * 3), name='dispatch')  
class Gallery(TemplateView):
    template_name = 'gallery/gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['moments'] = models.Moment.objects.all()
        print(models.Moment.objects.all())
        return context
    

    def post(self, request, *args, **kwargs):
        if request.FILES.get('img'):
            print(request.POST.get('id'))
            img = request.FILES.get('img')
            img_temporary = Image.open(img)
            
            # Resize image to 720p

            if img_temporary.mode == 'RGBA':
                img_temporary = img_temporary.convert('RGB')
            output_io_stream = BytesIO()
            img_temporary.save(output_io_stream, format='JPEG', quality=50)
            output_io_stream.seek(0)
            img2 = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.jpg" % img.name.split('.')[0], 'image/jpeg', output_io_stream.getbuffer().nbytes, None)
            moment = models.ImgMoment(
                 moment=models.Moment.objects.get(pk=int(request.POST.get('id'))),
                 img=img2)

            moment.save()

        if request.POST.get('delete'):
            img = models.ImgMoment.objects.get(pk=request.POST.get('delete'))
            img.delete()
        return self.render_to_response(self.get_context_data())
    


class MomentCreate(CreateView):
    model = models.Moment
    form_class = forms.Moment
    template_name = 'gallery/moment-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Guarda el objeto y redirige al éxito
        img = form.instance.img
        img_temporary = Image.open(img)
        
        # Resize image to 720p

        if img_temporary.mode == 'RGBA':
            img_temporary = img_temporary.convert('RGB')
        output_io_stream = BytesIO()
        img_temporary.save(output_io_stream, format='JPEG', quality=50)
        output_io_stream.seek(0)
        form.instance.img = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.jpg" % img.name.split('.')[0], 'image/jpeg', output_io_stream.getbuffer().nbytes, None)

        self.object = form.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:gallery')



class MomentUpdate(UpdateView):
    model = models.Moment
    form_class = forms.Moment
    template_name = 'gallery/moment-update.html'

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
        return reverse_lazy('estudios:gallery')



class MomentDelete(DeleteView):
    model = models.Moment
    template_name = 'gallery/moment-delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:gallery')








class Box(TemplateView):
    template_name = 'box/box.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            last_box = models.Box.objects.filter(open=False).latest('id')
            last_movimientos = models.Movements.objects.filter(box=last_box)
        except models.Box.DoesNotExist:
            last_movimientos = models.Movements.objects.none()

        try:
            box = models.Box.objects.get(open=True)
            movimientos = models.Movements.objects.filter(box=box)
        except models.Box.DoesNotExist:
            movimientos = models.Movements.objects.none()

        balance_apertura = 0
        ingresos = 0
        egresos = 0

        for movimiento in movimientos:
            if movimiento.type == 'ingreso':
                ingresos += movimiento.mount
            elif movimiento.type == 'gasto':
                egresos += movimiento.mount

        balance_caja = balance_apertura + ingresos - egresos
        total_ingresos = 0
        total_gastos = 0

        for movimiento in  models.Movements.objects.all():
            if movimiento.type == 'ingreso':
                total_ingresos += movimiento.mount
            elif movimiento.type == 'gasto':
                total_gastos += movimiento.mount

        last_ingreso = 0
        last_gasto = 0

        for movimiento in last_movimientos:
            if movimiento.type == 'ingreso':
                last_ingreso += movimiento.mount
            elif movimiento.type == 'gasto':
                last_gasto += movimiento.mount


        context['total_movimientos'] = total_ingresos - total_gastos

        context['total_last_session'] = last_ingreso - last_gasto

        context['is_open'] = models.Box.objects.filter(open=True).exists()
        context['movimientos'] = movimientos
        context['balance_apertura'] = balance_apertura
        context['ingresos'] = ingresos
        context['egresos'] = egresos
        context['balance_caja'] = balance_caja
        context['cajas'] = models.Box.objects.all()
        context['years'] = range(2025, 2028)  # Example range of years
        context['meses'] = [
                    {'numero': 1, 'nombre': 'Enero'},
                    {'numero': 2, 'nombre': 'Febrero'},
                    {'numero': 3, 'nombre': 'Marzo'},
                    {'numero': 4, 'nombre': 'Abril'},
                    {'numero': 5, 'nombre': 'Mayo'},
                    {'numero': 6, 'nombre': 'Junio'},
                    {'numero': 7, 'nombre': 'Julio'},
                    {'numero': 8, 'nombre': 'Agosto'},
                    {'numero': 9, 'nombre': 'Septiembre'},
                    {'numero': 10, 'nombre': 'Octubre'},
                    {'numero': 11, 'nombre': 'Noviembre'},
                    {'numero': 12, 'nombre': 'Diciembre'},
        ]
        return context

    def post(self, request, *args, **kwargs):
        tipo = request.POST.get('tipo')
        caja = request.POST.get('caja')
        year = request.POST.get('year')
        mes_inicio = request.POST.get('mes_inicio')
        mes_fin = request.POST.get('mes_fin')
        print(tipo)
        movimientos = models.Movements.objects.all()

        if tipo and tipo != 'todos':
            movimientos = movimientos.filter(type=tipo)

        if caja and caja != 'todas':
            movimientos = movimientos.filter(box=models.Box.objects.get(pk=int(caja)))

        if year and year != 'todos':
            movimientos = movimientos.filter(date__year=year)

        if mes_inicio and mes_inicio != 'todos':
            movimientos = movimientos.filter(date__month__gte=mes_inicio)

        if mes_fin and mes_fin != 'todos':
            movimientos = movimientos.filter(date__month__lte=mes_fin)

        balance_apertura = 0
        ingresos = 0
        egresos = 0

        for movimiento in movimientos:
            if movimiento.type == 'ingreso':
                ingresos += movimiento.mount
            elif movimiento.type == 'gasto':
                egresos += movimiento.mount

        balance_caja = balance_apertura + ingresos - egresos

        context = self.get_context_data()
        context['movimientos'] = movimientos
        context['balance_apertura'] = balance_apertura
        context['ingresos'] = ingresos
        context['egresos'] = egresos
        context['balance_caja'] = balance_caja

        return self.render_to_response(context)
    


class BoxCreate(TemplateView):
    model = models.Box
    template_name = 'box/box-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_open'] = models.Box.objects.filter(open=True).exists()
        return context


    def post(self, request, *args, **kwargs):
        if request.POST.get('open'):
            box = models.Box(
                user=request.user, created_box=timezone.now()
            )
            box.save()

            if request.POST.get('open_amount'):
                models.Movements(
                    user=request.user,
                    box=box,
                    mount=int(request.POST.get('open_amount').replace(',', '') or 0),
                    type='ingreso',
                    description='Apertura de caja'
                ).save()
        if request.POST.get('close'):
            box = models.Box.objects.filter(open=True).latest('id')
            box.open = False
            box.save()

        
        return redirect('estudios:box')
    


class Admin(TemplateView):
    template_name = 'admin/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = models.User.objects.all()
        return context



# Empleados
class Empleados(TemplateView):
    template_name = 'empleados/empleados.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empleados'] = models.User.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('role'):
            user = User.objects.get(pk=request.POST.get('id'))
            user.profile.role = request.POST.get('role')
            user.profile.save()
        return self.render_to_response(self.get_context_data())
    

class EmpleadoCreate(CreateView):
    model = User
    form_class = forms.User
    template_name = 'empleados/empleados-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.username = form.instance.email
        form.instance.first_name = form.instance.first_name
        form.instance.last_name = form.instance.last_name
        form.instance.set_password(form.instance.password)
        # Guarda el objeto y redirige al éxito
        self.object = form.save()
        models.Profile.objects.create(user=self.object, 
                estudio=self.request.user.profile.estudio)
        models.Config.objects.create(user=self.object)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:empleados')




class EmpleadoUpdate(UpdateView):
    model = User
    form_class = forms.User
    template_name = 'empleados/empleados-update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # Guarda el objeto y redirige al éxito
        form.instance.first_name = form.instance.first_name
        form.instance.last_name = form.instance.last_name
        form.instance.set_password(form.instance.password)
        self.object = form.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:empleados')
    



class EmpleadoDelete(DeleteView):
    model = User
    template_name = 'empleados/empleados-delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = models.User.objects.get(pk=self.kwargs.get('pk'))
        return context
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('delete'):
            user = models.User.objects.get(pk=self.kwargs.get('pk'))
            user.delete()
            return redirect('estudios:empleados')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('estudios:empleados')



class Login(TemplateView):
    template_name = 'login/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('estudios:dashboard')
        return super().get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if models.Estudios.objects.filter(name='ClickEstudios').exists():
            estudio = models.Estudios.objects.get(name='ClickEstudios')
            context['estudios'] = estudio
        return context
    

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('estudios:dashboard')
        messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        return self.render_to_response(self.get_context_data())


class Logout(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('estudios:login')
    


class ProfileClient(DetailView):
    model = models.Sale
    template_name = 'profile/profile-client.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = models.Service.objects.all()
        if models.ImgMoment.objects.exists():
                context['coro'] = True
                list_img = []
                for img in models.ImgMoment.objects.all():
                    list_img.append(img.id)
                random.shuffle(list_img)

                # Obtener una imagen aleatoria
                def Get_Img_Random(id):    
                    if id < len(list_img):
                        return models.ImgMoment.objects.filter(id=list_img[id]).first()
                    return None
                
                context['img1'] = Get_Img_Random(0)
                context['img2'] = Get_Img_Random(1)
                context['img3'] = Get_Img_Random(2)
                context['img4'] = Get_Img_Random(3)
                context['img5'] = Get_Img_Random(4)
                context['img6'] = Get_Img_Random(5)
                context['img7'] = Get_Img_Random(6)

        return context
    

class GastosCreate(TemplateView):
    template_name = 'gastos/gastos-create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gastos = models.Movements.objects.filter(type='gasto', 
            box=models.Box.objects.get(open=True))
        context['gastos'] = gastos
        context['total_gastos'] = sum(gasto.mount for gasto in gastos)

        return context

    def post(self, request, *args, **kwargs):
        gastos_data = request.POST.get('gastosData')
        if gastos_data:
            gastos = json.loads(gastos_data)
            for gasto in gastos:
                g =   models.Movements.objects.create(
                    user=request.user,
                    box=models.Box.objects.get(open=True),
                    mount= gasto['amount'],
                    type='gasto',
                    description=gasto['name'],
                )
                g.save()
                print(g)
              
        return redirect(self.get_success_url())

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:gastos-create')    
    

class FastSale(TemplateView):
    template_name = 'fast-sale/fast-sale.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('name'):
            models.Movements.objects.create(
                user=request.user,
                box=models.Box.objects.get(open=True),
                mount= int(request.POST.get('preci').replace(',', '')),
                type='ingreso',
                description= 'Pago completado ' + request.POST.get('name')  
            ).save()
        
            sale = models.Sale(
                name_client= request.POST.get('name'),
                name_plan='Venta rapida',
                price_plan=int(request.POST.get('preci').replace(',', '')),
                payment=True,
                saled_date = timezone.now(),
            )

            sale.save()
              
        return redirect(self.get_success_url(sale.id))

    def get_success_url(self, move):
        return reverse_lazy('estudios:estudios' , kwargs={'pk': move})

    

class Factura(TemplateView):
        template_name = 'factura/factura.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            sale = models.Sale.objects.get(id=self.kwargs.get('pk'))

            context['ncf'] =utils.GetNCF(sale.sale_type)
            sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))
            sale_itebis = sale.price_plan * 0.18
            total = sale.price_plan 
            if sale.sale_adicionales.all():
                for adicional in sale.sale_adicionales.all():
                    total += adicional.price


                

            total_itebis = total * 0.18
            context['total_itebis'] = total_itebis
            context['sale'] = sale
            if sale.discount:
                context['total_con_i'] = total 
            else:
                context['total_con_i'] = total + total_itebis

            context['total_sin'] = total
            context['total'] = total + total_itebis
            context['total_adicionales'] = total - sale.price_plan
            context['adicionales'] = sale.sale_adicionales.all()
            context['sale_itebis'] = sale_itebis
            context['sale_price_unitario'] = sale.price_plan + sale_itebis
            context['ncf'] =utils.GetNCF(sale.sale_type)
            return context


        def post(self, request, *args, **kwargs):
            sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))

            if request.POST.get('search_rnc'):
                sale.rnc_client = request.POST.get('search_rnc')
                sale.name_company_client = request.POST.get('search_name')
                sale.save()

                
            if request.POST.get('discount'):
                if sale.discount:
                    sale.discount = False
                    print(sale.discount)
                else:
                    sale.discount = True
                    print(sale.discount)

            
            if request.POST.get('invoice_type'):
                sale.sale_type = request.POST.get('invoice_type')
                if request.POST.get('invoice_type') == 'credito':
                    sale.discount = False
                    sale.save()

                
            if request.POST.get('search_name'):
                sale.sale_type = request.POST.get('search_name')


            # Finalizar venta
            if request.POST.get('end'):
                if sale.sale_type == 'credito':
                    sale.credito_fiscal = utils.GetNCF('credito')
                else:
                    sale.cosumidor_final = utils.GetNCF('consumidor')
                sale.finalize = True


       
            sale.save()
            return self.render_to_response(self.get_context_data())
        

# Mhia

class Mhia(TemplateView):
    template_name = 'mhia/mhia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    


class Configuration(TemplateView):
    template_name = 'configuration/configuration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if models.Estudios.objects.filter(name='ClickEstudios').exists():
            estudio = models.Estudios.objects.get(name='ClickEstudios')
            context['estudios'] = estudio
        return context
    

    def post(self, request, *args, **kwargs):
        if request.POST.get('mode'):
            config = models.Config.objects.get(user=request.user)
            if  config.mode:
                config.mode = False
            else:
                config.mode = True
            config.save()

        return self.render_to_response(self.get_context_data())
    


class Facturacion(TemplateView):
    template_name = 'facturacion/facturacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estudios = self.request.user.profile.estudio
        context['estudios'] =  estudios
        context['facturacion'] = models.Facturacion.objects.filter(estudio=estudios, payment=False).last()
        context['day_disponible'] = models.Facturacion.objects.filter(estudio=estudios, payment=False).last()
        if context['facturacion']:
            today = timezone.now().date()
            next_payment_date = context['facturacion'].next_payment_date
            context['days_remaining'] = (next_payment_date - today).days
        else:
            context['days_remaining'] = None
        return context
    

    def post(self, request, *args, **kwargs):
        if request.POST.get('name'):
            sale = models.Sale(
                name_plan=request.POST.get('name'),
                price_plan=int(request.POST.get('price').replace(',', '')),
                payment=True,
            )
            sale.save()
        return self.render_to_response(self.get_context_data())
    

class ListFacturacion(TemplateView):
    template_name = 'facturacion/list-facturacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estudios = self.request.user.profile.estudio
        context['estudios'] =  estudios
        context['facturaciones'] = models.Facturacion.objects.filter(estudio=estudios)
        return context
    

    def post(self, request, *args, **kwargs):
        if request.POST.get('name'):
            sale = models.Sale(
                name_plan=request.POST.get('name'),
                price_plan=int(request.POST.get('price').replace(',', '')),
                payment=True,
            )
            sale.save()
        return self.render_to_response(self.get_context_data())
    

class Contactos(TemplateView):
    template_name = 'contactos/contactos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] =  models.Contact.objects.all()
        return context    
    
class ContactoCreate(CreateView):
        model = models.Contact
        form_class = forms.Contact
        template_name = 'contactos/contacto-create.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

        def form_valid(self, form):
            self.object = form.save()
            return redirect(self.get_success_url())

        def form_invalid(self, form):
            print(form.errors)
            return self.render_to_response(self.get_context_data(form=form))

        def get_success_url(self):
            # Retorna la URL a la que redirigirá después de un submit exitoso
            return reverse_lazy('estudios:contactos')
        

class ContactoUpdate(UpdateView):
        model = models.Contact
        form_class = forms.Contact
        template_name = 'contactos/contacto-create.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

        def form_valid(self, form):
            self.object = form.save()
            return redirect(self.get_success_url())

        def form_invalid(self, form):
            print(form.errors)
            return self.render_to_response(self.get_context_data(form=form))

        def get_success_url(self):
            # Retorna la URL a la que redirigirá después de un submit exitoso
            return reverse_lazy('estudios:contactos')




class ContactoDelete(DeleteView):
    template_name = 'contactos/contacto-delete.html'
    model = models.Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        # Retorna la URL a la que redirigirá después de un submit exitoso
        return reverse_lazy('estudios:contactos')



class Facturas(TemplateView):
    template_name = 'factura/facturas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales = models.Sale.objects.filter(payment=True).order_by('-id')[:6]
        context['sales'] =   sales 
        return context


class Correos(TemplateView):
    template_name = 'correos/correos.html'


class OfertasService(TemplateView):
    template_name = 'service/oferta-service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = models.Service.objects.get(id=self.kwargs.get('pk'))
        context['plans'] = models.Plan.objects.filter(service__id=self.kwargs.get('pk'))
        context['admin'] = True
        context['0'] = 0
        return context
    

    def post(self, request, *args, **kwargs):
        service = models.Service.objects.get(id=self.kwargs.get('pk'))
        plans =  models.Plan.objects.filter(service__id=self.kwargs.get('pk'), is_offer=True)
        if request.POST.get('discount'):
            service.is_offer = True
            service.discount = int(request.POST.get('discount'))
            service.mount = 0
            service.save()
            for plan in plans:
                plan.mount = plan.price - (plan.price * service.discount / 100)
                plan.save()

        if request.POST.get('discount-custom'):
            mount = request.POST.get('discount-custom').replace(',', '')
            service.is_offer = True
            service.mount = int(mount)
            service.discount = 0
            service.save()
            for plan in plans:
                    
                    plan.mount = plan.price - int(mount)
                    plan.save()

        if request.POST.getlist('checking'):
            for id_plan in request.POST.getlist('checking'):
                plan = models.Plan.objects.get(id=int(id_plan))
                plan.is_offer = True
                if  service.discount > 0:
                    plan.mount = plan.price - (plan.price * service.discount / 100)
                if service.mount > 0:
                    plan.mount = plan.price - service.mount
                plan.save()

        if request.POST.getlist('checking-disabled'):
            for id_plan in request.POST.getlist('checking-disabled'):
                plan = models.Plan.objects.get(id=int(id_plan))
                plan.is_offer = False
                plan.save()
        return redirect('estudios:ofertas-service' , pk=service.id)