from django import forms
from .models import Backpack
from bootstrap_datepicker_plus import DatePickerInput


class BackpackForm(forms.ModelForm):

    class Meta:
        model = Backpack
        fields = ['place', 'start_date', 'end_date', 'sex']
        widgets = {
            'place': forms.TextInput(attrs={'placeholder': 'Paris, França', 'autofocus': 'autofocus'}),
            'start_date': DatePickerInput(),
            'end_date': DatePickerInput()
        }
        labels = {
            'place': "Para onde?",
            'start_date': "Data do começo",
            'end_date': "Data do fim",
            'sex': "Você se identifica como?"
        }
