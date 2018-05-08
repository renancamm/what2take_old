from django import forms
from .models import Backpack


class BackpackForm(forms.ModelForm):

    TEMP_CHOICES = (
        (0, 'Muito frio'),
        (10, 'Frio'),
        (20, 'Quente'),
        (30, 'Muito quente'),
    )
    DAYS_CHOICES = (
        (3, '3 dias'),
        (7, '7 dias'),
        (11, '11 dias'),
        (14, '+14 dias'),
    )
    SEX_CHOICES = (
        ('m', 'Homem'),
        ('f', 'Mulher'),
    )

    temp = forms.ChoiceField(label='Temperatura', choices=TEMP_CHOICES, widget=forms.RadioSelect())
    days = forms.ChoiceField(label='Dias', choices=DAYS_CHOICES, widget=forms.RadioSelect())
    sex = forms.ChoiceField(label='Sexo', choices=SEX_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Backpack
        fields = ('temp', 'days', 'sex')
