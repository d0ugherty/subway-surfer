from django import forms
from .models import *


class StationSlctForm(forms.Form):
    stop_choice = forms.ModelChoiceField(queryset=Stop.objects.all(), 
                                         label = "See Arrivals & Departures At: ",
                                         to_field_name='stop_name',
                                         required=False)

"""
    TO DO: Display routes depending on the Agency selected
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
            queryset=Route.objects.filter(agency_id=agency)
        )


    """ 
    route_choice = forms.ModelChoiceField(queryset=Route.objects.all(),
                                          label = "Select Route",
                                          to_field_name='route_long_name',
                                          required=True)
                                          """

    """   
    origin = forms.ModelChoiceField(queryset=Stop.objects.all(), 
                                         label = "Select Origin: ",
                                         to_field_name='stop_name',
                                         required=False)
    
    destination = forms.ModelChoiceField(queryset=Stop.objects.all(), 
                                         label = "Select Destination: ",
                                         to_field_name='stop_name',
                                         required=False)
"""
    
