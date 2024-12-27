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


class Dashboard(TemplateView):
    def get(self, request):
        return render(request, 'estudios/dashboard.html')


class Pos(TemplateView):
    template_name = 'pos/pos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_choices'] = models.Service.objects.all()
        context['plan_choices'] = models.Plan.objects.all()
        context['sales'] = models.Sale.objects.filter(is_reserve=False, finalize=False).order_by('-id')
        context['sales_reservers'] = models.Sale.objects.filter(is_reserve=True, finalize=False).order_by('-id')
        context['box_is_open'] = models.Box.objects.filter(open=True).exists() 
        context['today'] = timezone.now().date()
        context['time_now'] = timezone.now().strftime('%H:%M')
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


class SaleReserver(TemplateView):
    model = models.Sale
    form_class = forms.Sale
    template_name = 'sale/sale-reserver.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sale'] = models.Sale.objects.get(pk=self.kwargs.get('pk'))
        return context
    

    def post(self, request, *args, **kwargs):
        new_mount = request.POST.get('mount')
        if new_mount:
            sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))
            # Reservar la venta
            sale.is_reserve = True
            new_mount = int(new_mount)



            sale.mount = (sale.mount or 0) + int(new_mount)

            if sale.mount >= sale.price_plan:
                sale.mount = sale.price_plan
                sale.payment = True
                description = 'Pago completo'
            else:
                description = 'Abono'

            # Restar monto 
            sale.debit_mount -= new_mount

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
        return context

    def form_valid(self, form):
        plan_id = self.kwargs.get('pk')
        if plan_id:
            plan = models.Plan.objects.get(pk=plan_id)
            form.instance.name_plan = plan.name
            form.instance.debit_mount = plan.price
            form.instance.img = plan.img
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
                form.instance.name_plan = plan.name
                form.instance.debit_mount = plan.price
                form.instance.img = plan.img
                form.instance.description_plan = plan.description
                form.instance.price_plan = plan.price

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
        context['total_con_i'] = total 
        context['total_sin'] = total
        context['total'] = total - total_itebis
        context['total_adicionales'] = total - sale.price_plan
        context['adicionales'] = sale.sale_adicionales.all()
        context['sale_itebis'] = sale_itebis
        context['sale_price_unitario'] = sale.price_plan - sale_itebis
        return context



    def post(self, request, *args, **kwargs):
        # Agregar adicional
        if request.POST.get('name'):
            sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))
            a = models.Adicional(
                    sale=sale,
                    name= request.POST.get('name'),
                    description= request.POST.get('description'),
                    price= int(request.POST.get('price'))
            )
            a.save()

        # Eliminar adicional
        if request.POST.get('delete'):
                adicional = models.Adicional.objects.get(pk=request.POST.get('delete'))
                adicional.delete()
        
        # Finalizar venta
        if request.POST.get('end'):
            sale = models.Sale.objects.get(pk=self.kwargs.get('pk'))
            sale.finalize = True
            sale.save()
            return redirect('estudios:pos')
            
        return self.render_to_response(self.get_context_data())
    

class Gallery(TemplateView):
    template_name = 'gallery/gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['moments'] = models.Moment.objects.all()
        return context
    

    def post(self, request, *args, **kwargs):
        if request.FILES.get('img'):
            print(request.POST.get('id'))
            moment = models.ImgMoment(
                 moment=models.Moment.objects.get(pk=int(request.POST.get('id'))),
                 img=request.FILES['img'])
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











class Box(TemplateView):
    template_name = 'box/box.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movimientos = models.Movements.objects.all()
        balance_apertura = 0
        ingresos = 0
        egresos = 0

        for movimiento in movimientos:
            if movimiento.type == 'ingreso':
                ingresos += movimiento.mount
            elif movimiento.type == 'gasto':
                egresos += movimiento.mount

        balance_caja = balance_apertura + ingresos - egresos

        context['is_open'] = models.Box.objects.filter(open=True).exists()
        context['movimientos'] = movimientos
        context['balance_apertura'] = balance_apertura
        context['ingresos'] = ingresos
        context['egresos'] = egresos
        context['balance_caja'] = balance_caja
        context['cajas'] = models.Box.objects.all()
        context['years'] = range(2024, 2028)  # Example range of years
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
                user=request.user
            )
            box.save()
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
        

        # Create a profile for the new user

        
        # Guarda el objeto y redirige al éxito
        self.object = form.save()
        models.Profile.objects.create(user=self.object)
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
    template_name = 'empleados/empleados_confirm_delete.html'

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('estudios:dashboard')
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
        return context