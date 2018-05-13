from django import forms
from .models import Backpack


class BackpackForm(forms.ModelForm):

    temp = forms.ChoiceField(label='Como é o seu destino?', choices=Backpack.TEMP_CHOICES, initial=30, widget=forms.RadioSelect())
    days = forms.ChoiceField(label='Quanto tempo?', choices=Backpack.DAYS_CHOICES, initial=11, widget=forms.RadioSelect())
    sex = forms.ChoiceField(label='Você se vê como...', choices=Backpack.SEX_CHOICES, initial='f', widget=forms.RadioSelect())

    class Meta:
        model = Backpack
        fields = ('temp', 'days', 'sex')
