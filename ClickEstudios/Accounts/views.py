from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic import DeleteView
from django.urls import reverse_lazy


class ViewAccounts(TemplateView):
      template_name = "accounts/accounts/view-accounts.html"


class Login(LoginView):
    template_name = "accounts/login-accounts.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.get_redirect_url() or "/"

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos")
        return super().form_invalid(form)

class Logouts(TemplateView):
      template_name = "accounts/logout-accounts.html"

      def post(self, request, *args, **kwargs):
            logout(request)
            return redirect("/")



class CreateAccounts(CreateView):
    model = User
    form_class = User
    template_name = "accounts/accounts/create-accounts.html"

    def get_success_url(self):
        return redirect("/")



class UpdateAccouns(TemplateView):
    template_name = "accounts/accounts/update-accounts.html"

    def get_success_url(self):
        return self.request.path



class DeleteAccount(DeleteView):
    model = User
    template_name = "accounts/delete-accounts.html"
    success_url = reverse_lazy("home")
   

    def get_object(self, queryset=None):
        return self.request.user
    

    
    
