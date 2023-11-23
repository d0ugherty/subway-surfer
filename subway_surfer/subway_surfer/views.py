from .bcolors import bcolors
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import StationSlctForm
from .models import Stop
from .utils import validate_station_name
from .api import get_arrivals

from django.shortcuts import redirect

def home(request):
    station = "30th Street Station"
    print("this print statement is from home() function")
    print(request.method)
    if request.method == 'POST':
        form = StationSlctForm(request.POST)
        if form.is_valid():
            selected_stop = form.cleaned_data['stop_choice']
            stop_name = validate_station_name(selected_stop)
            # Redirect to the load_arrivals view with the selected stop_name
            return redirect('load_arrivals', station=stop_name)
    else:
        form = StationSlctForm()

    stops = Stop.objects.all()

    # Include 'station' in the context dictionary
    context = {'form': form, 'stops': stops, 'station': station}

    return render(request, 'home.html', context)


def select_stop(request):
    print("this print statement is from select_stop() !!")
    if request.method == 'POST':
        form = StationSlctForm(request.POST)
        if form.is_valid():
            selected_stop = form.cleaned_data['stop_choice']
            stop_name = validate_station_name(selected_stop)
            return redirect('load_arrivals', stop_name=stop_name)
    else:
        form = StationSlctForm()
    stops = Stop.objects.all()
    return render(request, 'arrivals.html', {'form': form,
                                    'stops': stops})

"""Render the Arrivals and Departures Table"""
def load_arrivals(request, station):
    arrival_context = get_arrivals(station)
    form = StationSlctForm() 
    return render(request, 'arrivals.html', {
        'arrivals_info': arrival_context,
        'station': station,
        'form': form 
    })

"""Update Arrivals"""
def update_arrivals_table(request):
    station = request.POST.get('station', "30th Street Station") 
    arrival_context = get_arrivals(station)
    html = render_to_string('table_rows.html', {'arrivals_info': arrival_context})
    return JsonResponse({'html': html})