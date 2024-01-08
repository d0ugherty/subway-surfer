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
    return render(request, 'info_board/arrivals.html', {'form': form, 'stops': stops})

"""Render the Arrivals and Departures Table"""
def load_arrivals(request, station):
    arrival_context = get_arrivals(station)
    print(arrival_context['arrivals_by_line']['Paoli/Thorndale'])

    form = StationSlctForm() 
    return render(request, 'info_board/arrivals.html', {
        'all_arrivals': arrival_context['all_arrivals'],
        'air_arrivals': arrival_context['arrivals_by_line']['Airport'],
        'che_arrivals': arrival_context['arrivals_by_line']['Chestnut Hill East'],
        'chw_arrivals': arrival_context['arrivals_by_line']['Chestnut Hill West'],
        'lan_arrivals': arrival_context['arrivals_by_line']['Lansdale/Doylestown'],
        'med_arrivals': arrival_context['arrivals_by_line']['Media/Wawa'],
        'fox_arrivals': arrival_context['arrivals_by_line']['Fox Chase'],
        'nor_arrivals': arrival_context['arrivals_by_line']['Manayunk/Norristown'],
        'pao_arrivals': arrival_context['arrivals_by_line']['Paoli/Thorndale'],
        'cyn_arrivals': arrival_context['arrivals_by_line']['Cynwyd'],
        'tre_arrivals': arrival_context['arrivals_by_line']['Trenton'],
        'war_arrivals': arrival_context['arrivals_by_line']['Warminster'],
        'wil_arrivals': arrival_context['arrivals_by_line']['Wilmington/Newark'],
        'wtr_arrivals': arrival_context['arrivals_by_line']['West Trenton'],
        'station': station,
        'form': form 
    })

"""Update Arrivals"""
def update_arrivals_table(request):
    station = request.POST.get('station', "30th Street Station") 
    arrival_context = get_arrivals(station)
    html = render_to_string('info_board/table_rows.html', {'all_arrivals': arrival_context['all_arrivals']})
    return JsonResponse({'html': html})