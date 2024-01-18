from django import forms
from .models import *


class StationSlctForm(forms.Form):
    stop_choice = forms.ModelChoiceField(queryset=Stop.objects.all(), 
                                         label = "See Arrivals & Departures At: ",
                                         to_field_name='stop_name',
                                         required=False)

"""
    TO DO: Display stops depending on route selected
"""

class AgencySlctForm(forms.Form):
    agency_choice = forms.ModelChoiceField(queryset=Agency.objects.all(),
                                           label = "Select Agency",
                                           to_field_name='agency_name',
                                           required=True)
    
class RouteSlctForm(forms.Form):
    def __init__(self, agency, *args, **kwargs):
        super(RouteSlctForm, self).__init__(*args, **kwargs)
        self.fields['routes'] = forms.ModelChoiceField(
            queryset=Route.objects.filter(agency_id=agency),
            required=False
        )
    

class OriginForm(forms.Form):
       
    origin_choice = forms.ModelChoiceField(queryset=Stop.objects.all(), 
                                         label = "Select Origin: ",
                                         to_field_name='stop_name',
                                         required=False)
    
class DestForm(forms.Form):

    def __init__(self, origin, *args, **kwargs):
        super(DestForm, self).__init__(*args, **kwargs)
        self.fields['stops'] = forms.ModelChoiceField(
            queryset=Stop.objects.all().exclude(stop_id=origin), 
                                         label = "Select Destination: ",
                                         to_field_name='stop_name',
                                         required=False)

    
