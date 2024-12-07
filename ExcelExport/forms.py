from django import forms

class VentasForm(forms.Form):
    tipo_documento = forms.CharField(label="Tipo de Documento", max_length=50)
    total_documentos = forms.IntegerField(label="Total de Documentos")
    monto_exento = forms.DecimalField(label="Monto Exento", max_digits=10, decimal_places=2, required=False)
    monto_neto = forms.DecimalField(label="Monto Neto", max_digits=10, decimal_places=2)
    monto_iva = forms.DecimalField(label="Monto IVA", max_digits=10, decimal_places=2)
    monto_total = forms.DecimalField(label="Monto Total", max_digits=10, decimal_places=2)

class ComprasForm(forms.Form):
    numero_operacion = forms.IntegerField(label="Número de Operación")
    tipo_documento = forms.CharField(label="Tipo de Documento", max_length=50)
    tipo_compra = forms.CharField(label="Tipo de Compra", max_length=50)
    rut_proveedor = forms.CharField(label="RUT Proveedor", max_length=12)
    razon_social = forms.CharField(label="Razón Social", max_length=100)
    folio = forms.IntegerField(label="Folio")
    fecha_documento = forms.DateField(label="Fecha del Documento", widget=forms.DateInput(attrs={'type': 'date'}))
    monto_exento = forms.DecimalField(label="Monto Exento", max_digits=10, decimal_places=2, required=False)
    monto_total = forms.DecimalField(label="Monto Total", max_digits=10, decimal_places=2)
