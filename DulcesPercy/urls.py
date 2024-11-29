from django.contrib import admin
from django.urls import path
from ExcelExport.views import excel_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("excel/", excel_view, name="excel_view"),
]