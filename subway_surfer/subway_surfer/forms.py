from django import forms
from .models import *


class StationSlctForm(forms.Form):
    stop_choice = forms.ModelChoiceField(queryset=Stop.objects.all(), 
                                         label = "See Arrivals & Departures At: ",
                                         to_field_name='stop_name',
                                         required=False)

class AgencySlctForm(forms.Form):
    agency_choice = forms.ModelChoiceField(queryset=Agency.objects.all(),
                                           label = "Select Agency",
                                           to_field_name='agency',
                                           required=True)
"""
    TO DO: Display routes depending on the Agency selected
"""
class RouteSlctForm(forms.Form):
    route_choice = forms.ModelChoiceField(queryset=Route.objects.all(),
                                          label = "Select Route",
                                          to_field_name='route',
                                          required=True)

    
