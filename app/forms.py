from django import forms
from .models import Backpack
from bootstrap_datepicker_plus import DatePickerInput


class BackpackForm(forms.ModelForm):

    class Meta:
        model = Backpack
        fields = ['place', 'start_date', 'end_date', 'sex']
        widgets = {
            'start_date': DatePickerInput(),
            'end_date': DatePickerInput()
        }
