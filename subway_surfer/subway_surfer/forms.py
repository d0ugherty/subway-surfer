from django import forms
from .models import Stop


class StationSlctForm(forms.Form):
    stop_choice = forms.ModelChoiceField(queryset=Stop.objects.all(), 
                                         label = "See Arrivals & Departures At: ",
                                         to_field_name='stop_name',
                                         required=False)

    
