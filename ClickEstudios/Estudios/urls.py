
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'estudios'
urlpatterns = [
      path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
      path('pos/', views.Pos.as_view(), name='pos'),
      path('service/', views.Service.as_view(), name='service'),
      path('service-create/', views.ServiceCreate.as_view(), name='service-create'),
      path('service/<int:pk>/', views.ServiceDetail.as_view(), name='service-detail'),
      path('service-update/<int:pk>/', views.ServiceUpdate.as_view(), name='service-update'),
      path('service-delete/<int:pk>/', views.ServiceDelete.as_view(), name='service-delete'),
]
