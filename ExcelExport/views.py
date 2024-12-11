import openpyxl
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import VentasForm, ComprasForm, LibroDiarioForm
import pandas as pd
from django.http import FileResponse
import os
from django.conf import settings
from decimal import Decimal
def descargar_libro(request, tipo):
    if tipo == "ventas":
        path = os.path.join(settings.BASE_DIR, "REGISTRO DE VENTAS 2024.xlsx")
        filename = "REGISTRO DE VENTAS 2024.xlsx"
    elif tipo == "compras":
        path = os.path.join(settings.BASE_DIR, "REGISTRO DE COMPRAS 2024.xlsx")
        filename = "REGISTRO DE COMPRAS 2024.xlsx"
    elif tipo == "libro_diario":
        path = os.path.join(settings.BASE_DIR, "LDE.xlsx")
        filename = "LDE.xlsx"
    elif tipo == "balance":
        # Generar el archivo Balance a partir de la hoja 'Balance' en 'Contab 2024.xlsx'
        contab_path = os.path.join(settings.BASE_DIR, "Contab 2024.xlsx")
        if not os.path.exists(contab_path):
            return HttpResponse("El archivo 'Contab 2024.xlsx' no existe.", status=404)

        wb = openpyxl.load_workbook(contab_path,data_only=True)
        if 'BALANCE' not in wb.sheetnames:
            return HttpResponse("La hoja 'BALANCE' no existe en 'BALANCE.xlsx'.", status=404)

        balance_sheet = wb['BALANCE']

        # Crear un nuevo libro de Excel y copiar la hoja 'Balance'
        new_wb = openpyxl.Workbook()
        new_ws = new_wb.active
        new_ws.title = 'BALANCE'

        for row in balance_sheet.iter_rows(values_only=True):
            new_ws.append(row)

        # Guardar el nuevo libro en un objeto BytesIO
        from io import BytesIO
        output = BytesIO()
        new_wb.save(output)
        output.seek(0)

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=Balance.xlsx'
        return response
    else:
        return HttpResponse("Tipo de archivo no válido.", status=400)

    if os.path.exists(path):
        return FileResponse(open(path, 'rb'), as_attachment=True, filename=filename)
    else:
        return HttpResponse("El archivo no existe.", status=404)
def registro_ventas(request):
    if request.method == "POST":
        form = VentasForm(request.POST)
        if form.is_valid():
            # Cargar archivo Excel
            ventas_path = "REGISTRO DE VENTAS 2024.xlsx" 
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
            else:
                # Si ya existe la fórmula de suma, actualiza el rango para incluir la nueva fila
                for col in ['J', 'K', 'L']:
                    formula = ws[f"{col}{total_row}"].value
                    if formula:
                        # Actualizar el rango de la fórmula para incluir la nueva fila
                        new_formula = formula.replace(f"J{total_row - 1}", f"J{total_row}")
                        ws[f"{col}{total_row}"].value = new_formula
            
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
            ws[f"J{new_row}"] = form.cleaned_data['monto_total'] - (form.cleaned_data['monto_total'] * Decimal('0.19'))
            ws[f"K{new_row}"] = form.cleaned_data['monto_total'] * Decimal('0.19') 
            ws[f"L{new_row}"] = form.cleaned_data['monto_total']

            # Guardar el archivo
            wb.save(compras_path)
            return redirect('registro_compras')
    else:
        form = ComprasForm()
    return render(request, 'registro_compras.html', {'form': form})

def libro_diario(request):
    if request.method == "POST":
        form = LibroDiarioForm(request.POST)
        if form.is_valid():
            lde_path = os.path.join(settings.BASE_DIR, "LDE.xlsx")
            wb = openpyxl.load_workbook(lde_path)
            ws = wb.active

            # Buscar la última fila con datos reales a partir de la fila 3
            last_data_row = None
            for row in range(3, ws.max_row + 1):
                cell_value = ws[f"A{row}"].value  # Usamos la columna 'A' (fecha) como referencia
                if cell_value is None:
                    last_data_row = row - 1  # La fila anterior tiene datos
                    break
            else:
                # Si no hay filas vacías hasta el final, la última fila con datos es ws.max_row
                last_data_row = ws.max_row

            # Determinar la nueva fila para insertar datos
            new_row = last_data_row + 1

            # Calcular el total (suma de debe y haber)
            debe = form.cleaned_data['debe'] or Decimal('0')
            haber = form.cleaned_data['haber'] or Decimal('0')

            # Obtener 'Comp' inicial (primera letra del tipo de movimiento)
            tipo_movimiento = form.cleaned_data['tipo_movimiento']
            comp = tipo_movimiento[0].upper()  # 'T', 'E', 'I'

            # Calcular 'N°' correspondiente al 'Comp' actual
            # Inicializamos el contador en 1 si no hay registros previos
            comp_numbers = []
            for row in range(3, last_data_row + 1):
                cell_comp = ws[f"B{row}"].value  # Columna 'B' (Comp)
                cell_number = ws[f"C{row}"].value  # Columna 'C' (N°)
                if cell_comp == comp and isinstance(cell_number, int):
                    comp_numbers.append(cell_number)
            if comp_numbers:
                next_number = max(comp_numbers) + 1
            else:
                next_number = 1

            # Insertar los datos en la nueva fila
            ws[f"A{new_row}"] = form.cleaned_data['fecha']
            ws[f"B{new_row}"] = comp  # Columna 'Comp'
            ws[f"C{new_row}"] = next_number  # Columna 'N°'
            ws[f"D{new_row}"] = form.cleaned_data['nombre_cuenta']
            ws[f"E{new_row}"] = form.cleaned_data['glosa']
            ws[f"F{new_row}"] = debe
            ws[f"G{new_row}"] = haber

            # Actualizar las fórmulas en F1 y G1
            ws['F1'] = f"=SUM(F3:F{new_row})"
            ws['G1'] = f"=SUM(G3:G{new_row})"

            # Guardar el archivo Excel
            wb.save(lde_path)
            return redirect('libro_diario')
    else:
        form = LibroDiarioForm()
    return render(request, 'libro_diario.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def ver_registro(request):
    # Lista de libros disponibles
    libros = [
        {'nombre': 'Registro de Ventas 2024', 'tipo': 'ventas'},
        {'nombre': 'Registro de Compras 2024', 'tipo': 'compras'},
        {'nombre': 'Libro Diario', 'tipo': 'libro_diario'},
        {'nombre': 'Balance', 'tipo': 'balance'},
    ]
    return render(request, 'ver_registro.html', {'libros': libros})