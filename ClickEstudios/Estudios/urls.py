
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'estudios'
urlpatterns = [
      path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
            path('pos/', views.Pos.as_view(), name='pos'),


# Estudios
      path('estudios/<int:pk>', views.Estudios.as_view(), name='estudios'),

     
# Servcios
      path('service/', views.Service.as_view(), name='service'),
            path('service-create/', views.ServiceCreate.as_view(), name='service-create'),
                        path('service-detail/<int:pk>/', views.ServiceDetail.as_view(), name='service-detail'),
                  path('service-update/<int:pk>/', views.ServiceUpdate.as_view(), name='service-update'),
      path('service-delete/<int:pk>/', views.ServiceDelete.as_view(), name='service-delete'),


# Planes
      path('plan/', views.Plan.as_view(), name='plan'),
            path('plan-create/', views.PlanCreate.as_view(), name='plan-create'),
                        path('plan/<int:pk>/', views.PlanDetail.as_view(), name='plan-detail'),
                  path('plan-update/<int:pk>/', views.PlanUpdate.as_view(), name='plan-update'),
      path('plan-delete/<int:pk>/', views.PlanDelete.as_view(), name='plan-delete'),


# Ventas
      path('sale/', views.Sale.as_view(), name='sale'),
            path('sale-create/<int:pk>', views.SaleCreate.as_view(), name='sale-create'),
                        path('sale/<int:pk>/', views.SaleReserver.as_view(), name='sale-reserver'),
                  path('sale-update/<int:pk>/', views.SaleUpdate.as_view(), name='sale-update'),
]
