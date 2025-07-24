from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
      path('account', views.ViewAccounts.as_view(), name='accounts'),
            path('login/', views.Login.as_view(), name='login-accounts'),
                  path('logout/', views.Logouts.as_view(), name='logout'),
                        path('delete-account/<int:pk>/', views.DeleteAccount.as_view(), name='delete-account'),

      path('create-accounts/', views.CreateAccounts.as_view(), name='create-accounts'),
            path('update-accounts/<int:pk>/', views.UpdateAccouns.as_view(), name='update-accounts'),
                  
]
