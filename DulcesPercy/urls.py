from django.urls import path
from ExcelExport import views
from django.http import FileResponse
from django.http import HttpResponse

urlpatterns = [
    path('descargar/<str:tipo>/', views.descargar_libro, name='descargar_libro'),
    path('librodiario/', views.libro_diario, name='libro_diario'),
    path('', views.home, name='home'),
    path('registro/', views.ver_registro, name='ver_registro'),
]
