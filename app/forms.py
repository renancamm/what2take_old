from django import forms
from .models import Backpack


class BackpackForm(forms.ModelForm):

    class Meta:
        model = Backpack
        fields = ('temp', 'days', 'sex')
