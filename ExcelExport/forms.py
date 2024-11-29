from django import forms

class DataForm(forms.Form):
    razon_social = forms.CharField(label='Razón Social', max_length=100)
    rut = forms.CharField(label='RUT', max_length=20)
    direccion = forms.CharField(label='Dirección', max_length=200)
    tipo_comprobante = forms.ChoiceField(
        label='Tipo de Comprobante',
        choices=[('1', 'Ingreso'), ('2', 'Egreso')]
    )
    fecha = forms.DateField(
        label='Fecha (DD/MM/YYYY)',
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y')
    )
    codigo_cuenta = forms.CharField(label='Código de Cuenta', max_length=20)
    detalle = forms.ChoiceField(
        label='Detalle',
        choices=[('Compra', 'Compra'), ('Venta', 'Venta')]
    )
    monto = forms.FloatField(label='Monto')