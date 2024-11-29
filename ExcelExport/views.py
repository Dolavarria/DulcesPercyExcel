from django.shortcuts import render
from .forms import DataForm
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Border, Side
from datetime import datetime
from django.http import HttpResponse
import os
import io  # Ensure this import is present
from django.conf import settings
# Define the paths to the Excel files
archivo_registro = 'registro.xlsx'
archivo_compras = 'REGISTRO DE COMPRAS 2024.xlsx'
meses = {
    2: 'FEB',
    3: 'MAR',
    4: 'ABR',
    5: 'MAY',
    6: 'JUN',
    7: 'JUL',
    8: 'AGO',
    9: 'SEP'
}
border = Border(
    left=Side(border_style='thin', color='000000'),
    right=Side(border_style='thin', color='000000'),
    top=Side(border_style='thin', color='000000'),
    bottom=Side(border_style='thin', color='000000')
)

def inicializar_registro():
    if not os.path.exists(archivo_registro):
        wb = Workbook()
        ws = wb.active
        ws.append(["Razon Social", "RUT", "Direccion", "Tipo Comprobante", "Fecha", "Codigo Cuenta", "Detalle", "Monto"])
        wb.save(archivo_registro)

def inicializar_compras():
    if not os.path.exists(archivo_compras):
        wb = Workbook()
        sheet_names = ['FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP']
        for idx, sheet in enumerate(sheet_names):
            if idx == 0:
                ws = wb.active
                ws.title = sheet
            else:
                ws = wb.create_sheet(title=sheet)
            ws.append([
                "N°", "Tipo Doc", "Tipo Compra", "RUT Proveedor", "Razon Social",
                "Folio", "Fecha Docto", "Monto Exento", "Monto Neto",
                "Monto IVA Recuperable", "Monto Total"
            ])
            # Apply border to header row
            for col in range(1, 12):
                ws.cell(row=1, column=col).border = border
        wb.save(archivo_compras)

def obtener_proximo_numero(ws):
    if ws.max_row < 2:
        return 1
    else:
        ultimo_num = ws.cell(row=ws.max_row, column=2).value  # Adjusted column index
        return ultimo_num + 1 if isinstance(ultimo_num, int) else 1

def excel_view(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            razon_social = form.cleaned_data['razon_social']
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            tipo_comprobante = form.cleaned_data['tipo_comprobante']
            fecha_obj = form.cleaned_data['fecha']
            fecha = fecha_obj.strftime('%d/%m/%Y')
            codigo_cuenta = form.cleaned_data['codigo_cuenta']
            detalle = form.cleaned_data['detalle']
            monto = form.cleaned_data['monto']

            # Initialize Excel files if they don't exist
            inicializar_registro()
            inicializar_compras()

            # Save data to 'registro.xlsx'
            wb_registro = load_workbook(archivo_registro)
            ws_registro = wb_registro.active
            tipo = 'Debe' if tipo_comprobante == '1' else 'Haber'
            ws_registro.append([
                razon_social, rut, direccion, tipo, fecha,
                codigo_cuenta, detalle, monto
            ])
            wb_registro.save(archivo_registro)

            # Determine the sheet based on the month
            mes = fecha_obj.month
            hoja = meses.get(mes)
            if not hoja:
                return HttpResponse(f"Mes {mes} no soportado en 'REGISTRO DE COMPRAS 2024.xlsx'.")

            # Save data to 'REGISTRO DE COMPRAS 2024.xlsx'
            wb_compras = load_workbook(archivo_compras)
            ws_compras = wb_compras[hoja]

            proximo_num = obtener_proximo_numero(ws_compras)
            monto_neto = round(monto * 0.81, 2)
            monto_iva = round(monto * 0.19, 2)
            monto_total = monto

            ws_compras.append([
                "",                      # Columna A vacía
                proximo_num,             # N°
                33,                      # Tipo Doc
                "Del Giro",              # Tipo Compra
                rut,                     # RUT Proveedor
                razon_social,            # Razón Social
                codigo_cuenta,           # Folio
                fecha,                   # Fecha Docto
                "",                      # Monto Exento
                monto_neto,              # Monto Neto
                monto_iva,               # Monto IVA Recuperable
                monto_total              # Monto Total
            ])

            # Apply borders to the new row
            new_row = ws_compras.max_row
            for col in range(1, 12):  # Columns A to K
                cell = ws_compras.cell(row=new_row, column=col)
                cell.border = border

            # Save the updated 'REGISTRO DE COMPRAS 2024.xlsx'
            wb_compras.save(archivo_compras)

            # Now, return the updated 'REGISTRO DE COMPRAS 2024.xlsx' as a downloadable file
            with open(archivo_compras, 'rb') as fh:
                response = HttpResponse(
                    fh.read(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename="REGISTRO DE COMPRAS 2024.xlsx"'
                return response
    else:
        form = DataForm()
    return render(request, 'excel_form.html', {'form': form})