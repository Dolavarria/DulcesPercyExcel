import openpyxl
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import VentasForm, ComprasForm
import pandas as pd
from django.http import FileResponse
import os
from django.conf import settings
def descargar_libro(request, tipo):
    if tipo == "ventas":
        path = "REGISTRO DE VENTAS 2024.xlsx"
    elif tipo == "compras":
        path = "REGISTRO DE COMPRAS 2024.xlsx"
    else:
        return HttpResponse("Tipo de archivo no válido.", status=400)

    return FileResponse(open(path, 'rb'), as_attachment=True, filename=f"{tipo}_actualizado.xlsx")
def registro_ventas(request):
    if request.method == "POST":
        form = VentasForm(request.POST)
        if form.is_valid():
            # Cargar archivo Excel
            ventas_path = "REGISTRO DE VENTAS 2024.xlsx"  # Actualiza con la ruta correcta
            wb = openpyxl.load_workbook(ventas_path)
            ws = wb.active

            # Buscar la primera fila vacía
            for row in ws.iter_rows(min_row=5, max_row=ws.max_row+1):
                if all(cell.value is None for cell in row):
                    new_row = row[0].row
                    break
            
            # Insertar los datos en la primera fila vacía
            ws[f"B{new_row}"] = form.cleaned_data['tipo_documento']
            ws[f"C{new_row}"] = form.cleaned_data['total_documentos']
            ws[f"D{new_row}"] = form.cleaned_data['monto_exento'] or 0
            ws[f"E{new_row}"] = form.cleaned_data['monto_neto']
            ws[f"F{new_row}"] = form.cleaned_data['monto_iva']
            ws[f"G{new_row}"] = form.cleaned_data['monto_total']

            # Guardar el archivo
            wb.save(ventas_path)
            return redirect('registro_ventas')
    else:
        form = VentasForm()
    return render(request, 'registro_ventas.html', {'form': form})

def registro_compras(request):
    if request.method == "POST":
        form = ComprasForm(request.POST)
        if form.is_valid():
            compras_path = os.path.join(settings.BASE_DIR, "REGISTRO DE COMPRAS 2024.xlsx")
            wb = openpyxl.load_workbook(compras_path)
            
            # Obtener el mes de 'fecha_documento'
            fecha_doc = form.cleaned_data['fecha_documento']
            mes_numero = fecha_doc.month
            # Mapeo de mes a nombre de hoja
            meses = {
                1: 'ENER', 2: 'FEB', 3: 'MAR', 4: 'ABR',
                5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AGO',
                9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DIC'
            }
            nombre_hoja = meses.get(mes_numero)
            
            # Verificar si la hoja existe
            if nombre_hoja in wb.sheetnames:
                ws = wb[nombre_hoja]
            else:
                return HttpResponse(f"El libro no cubre el mes indicado: {nombre_hoja}", status=400)
            
            # Buscar la fila que contiene la fórmula de suma en la columna J
            total_row = None
            for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
                cell = row[9]  # Columna J es la décima columna (índice 9)
                if cell.data_type == 'f' and 'SUM' in str(cell.value):
                    total_row = cell.row
                    break
            
            if total_row is None:
                # Si no se encuentra la fila de totales, agregarla al final
                total_row = ws.max_row + 1
                ws[f"I{total_row}"] = 'Total'
                ws[f"J{total_row}"] = f"=SUM(J5:J{total_row - 1})"
                ws[f"K{total_row}"] = f"=SUM(K5:K{total_row - 1})"
                ws[f"L{total_row}"] = f"=SUM(L5:L{total_row - 1})"

            # Determinar la nueva fila para insertar datos (justo antes de la fila de totales)
            new_row = total_row

            # Insertar una nueva fila antes de la fila de totales
            ws.insert_rows(new_row)

            # Insertar los datos en la nueva fila
            ws[f"B{new_row}"] = form.cleaned_data['numero_operacion']
            ws[f"C{new_row}"] = form.cleaned_data['tipo_documento']
            ws[f"D{new_row}"] = form.cleaned_data['tipo_compra']
            ws[f"E{new_row}"] = form.cleaned_data['rut_proveedor']
            ws[f"F{new_row}"] = form.cleaned_data['razon_social']
            ws[f"G{new_row}"] = form.cleaned_data['folio']
            ws[f"H{new_row}"] = form.cleaned_data['fecha_documento']
            ws[f"I{new_row}"] = form.cleaned_data['monto_exento'] or 0
            ws[f"J{new_row}"] = form.cleaned_data['monto_neto']
            ws[f"K{new_row}"] = form.cleaned_data['monto_iva']
            ws[f"L{new_row}"] = form.cleaned_data['monto_total']

            # Guardar el archivo
            wb.save(compras_path)
            return redirect('registro_compras')
    else:
        form = ComprasForm()
    return render(request, 'registro_compras.html', {'form': form})
def resumen_datos(request):
    ventas_path = "REGISTRO_DE_VENTAS.xlsx"
    compras_path = "REGISTRO_DE_COMPRAS.xlsx"

    # Leer archivos
    ventas_df = pd.read_excel(ventas_path, skiprows=4)  # Ajusta si es necesario
    compras_df = pd.read_excel(compras_path, skiprows=4)  # Ajusta si es necesario

    # Sumar montos
    total_ventas = ventas_df['Monto Total'].sum()
    total_compras = compras_df['Monto Total'].sum()

    return render(request, 'registros/resumen.html', {
        'total_ventas': total_ventas,
        'total_compras': total_compras
    })
