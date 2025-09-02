from django import forms

class AirportDistanceForm(forms.Form):
    aeropuerto_origen = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: BOG',
            'class': 'form-control',
            'pattern': '[A-Z]{3}',
            'title': 'Código IATA de origen'
        }),
        label='Aeropuerto de origen'
    )
    aeropuerto_destino = forms.CharField(
        max_length=3,
        min_length=3,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: ANF',
            'class': 'form-control',
            'pattern': '[A-Z]{3}',
            'title': 'Código IATA de destino'
        }),
        label='Aeropuerto de destino'
    )
    def clean_aeropuerto_origen(self):
        codigo = self.cleaned_data['aeropuerto_origen']
        if len(codigo) != 3 or not codigo.isalpha() or not codigo.isupper():
            raise forms.ValidationError("El código de aeropuerto debe tener 3 letras mayúsculas.")
        return codigo
    def clean_aeropuerto_destino(self):
        codigo = self.cleaned_data['aeropuerto_destino']
        if len(codigo) != 3 or not codigo.isalpha() or not codigo.isupper():
            raise forms.ValidationError("El código de aeropuerto debe tener 3 letras mayúsculas.")
        return codigo