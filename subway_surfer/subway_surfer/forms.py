from django import forms
from .models import *


class StationSlctForm(forms.Form):
    stop_choice = forms.ModelChoiceField(queryset=Agency.get_agency('SEPTA').get_stops(), 
                                         label = "Select Station ",
                                         to_field_name='stop_name',
                                         required=False)

class AgencySlctForm(forms.Form):
    agency_choice = forms.ModelChoiceField(queryset=Agency.objects.all(),
                                           label = "Select Agency",
                                           to_field_name='agency_name',
                                           required=False)
    form_type = forms.CharField(widget=forms.HiddenInput(), initial='agency')
    
class RouteSlctForm(forms.Form):
    def __init__(self, agency, *args, **kwargs):
        super(RouteSlctForm, self).__init__(*args, **kwargs)
        self.fields['routes'] = forms.ModelChoiceField(
            queryset=Route.objects.filter(agency_id=agency),
            required=False
        )
    
    form_type = forms.CharField(widget=forms.HiddenInput(), initial='route')
    

class OriginForm(forms.Form):
    origin_choice = forms.ModelChoiceField(queryset=Stop.objects.all(), 
                                         label = "Select Origin: ",
                                         to_field_name='stop_name',
                                         required=False)
    
    form_type = forms.CharField(widget=forms.HiddenInput(), initial='origin')

class DestForm(forms.Form):

    def __init__(self, origin, *args, **kwargs):
        super(DestForm, self).__init__(*args, **kwargs)
        self.fields['stops'] = forms.ModelChoiceField(
            queryset=Stop.objects.all().exclude(stop_id=origin), 
                                         label = "Select Destination: ",
                                         to_field_name='stop_name',
                                         required=False)
        
    form_type = forms.CharField(widget=forms.HiddenInput(), initial='destination')

class AgencyCheckBox(forms.Form):
    show_septa = forms.BooleanField(initial=True, label="Show SEPTA", required=False)
    show_njt = forms.BooleanField(initial=False, label="Show NJT", required=False)
