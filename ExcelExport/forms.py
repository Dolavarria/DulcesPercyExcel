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


from django import forms

class LibroDiarioForm(forms.Form):
    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    tipo_movimiento = forms.ChoiceField(
        label="Tipo de Movimiento",
        choices=[
            ('Traspaso', 'Traspaso'),
            ('Egreso', 'Egreso'),
            ('Ingreso', 'Ingreso'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    nombre_cuenta = forms.CharField(
        label="Nombre de Cuenta",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    glosa = forms.CharField(
        label="Glosa o Detalle",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    debe = forms.DecimalField(
        label="Debe",
        max_digits=15,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    haber = forms.DecimalField(
        label="Haber",
        max_digits=15,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
