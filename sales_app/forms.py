from django import forms

class SaleForm(forms.Form):
    product = forms.CharField(max_length=100, label='Товар')
    price = forms.FloatField(min_value=0, label='Цена')
    quantity = forms.IntegerField(min_value=1, label='Количество')
    date = forms.DateField(label='Дата продажи', widget=forms.DateInput(attrs={'type': 'date'}))