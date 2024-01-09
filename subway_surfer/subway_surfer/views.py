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
    return render(request, 'info_board/arrivals.html', {
        'form': form, 
        'stops': stops})

"""Render the Arrivals and Departures Table"""
def load_arrivals(request, station):
    arrival_context = get_arrivals(station)
    print(f'FROM LOAD: {arrival_context}')

    form = StationSlctForm() 
    return render(request, 'info_board/arrivals.html', {
        'all_arrivals_ctx': arrival_context['all_arrivals_ctx'],
        'air_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Airport'],
        'che_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Chestnut Hill East'],
        'chw_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Chestnut Hill West'],
        'lan_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Lansdale/Doylestown'],
        'med_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Media/Wawa'],
        'fox_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Fox Chase'],
        'nor_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Manayunk/Norristown'],
        'pao_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Paoli/Thorndale'],
        'cyn_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Cynwyd'],
        'tre_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Trenton'],
        'war_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Warminster'],
        'wil_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Wilmington/Newark'],
        'wtr_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['West Trenton'],
        'station': station,
        'form': form 
    })


"""Update Arrivals"""
def update_arrivals_table(request):
    print(request.method)
    station = request.POST.get('station', "30th Street Station") 
    arrival_context = get_arrivals(station)
    print(f'FROM UPDATE: {arrival_context}')
    html = render_to_string('info_board/table_rows.html', {
        'all_arrivals_ctx': arrival_context['all_arrivals_ctx'],
        'air_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Airport'],
        'che_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Chestnut Hill East'],
        'chw_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Chestnut Hill West'],
        'lan_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Lansdale/Doylestown'],
        'med_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Media/Wawa'],
        'fox_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Fox Chase'],
        'nor_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Manayunk/Norristown'],
        'pao_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Paoli/Thorndale'],
        'cyn_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Cynwyd'],
        'tre_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Trenton'],
        'war_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Warminster'],
        'wil_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Wilmington/Newark'],
        'wtr_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['West Trenton'],
        'station': station,})
    return JsonResponse({'html': html})