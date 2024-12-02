from django.urls import path
from ExcelExport import views
from django.http import FileResponse
from django.http import HttpResponse

urlpatterns = [
    path('ventas/', views.registro_ventas, name='registro_ventas'),
    path('compras/', views.registro_compras, name='registro_compras'),
    path('descargar/<str:tipo>/', views.descargar_libro, name='descargar_libro'),

]
