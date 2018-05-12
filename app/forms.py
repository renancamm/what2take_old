from django import forms
from .models import Backpack


class BackpackForm(forms.ModelForm):

    temp = forms.ChoiceField(label='Temperatura', choices=Backpack.TEMP_CHOICES, initial=20, widget=forms.RadioSelect())
    days = forms.ChoiceField(label='Dias', choices=Backpack.DAYS_CHOICES, initial=7, widget=forms.RadioSelect())
    sex = forms.ChoiceField(label='Sexo', choices=Backpack.SEX_CHOICES, initial='f', widget=forms.RadioSelect())

    class Meta:
        model = Backpack
        fields = ('temp', 'days', 'sex')
