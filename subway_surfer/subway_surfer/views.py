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

"""
Render the Arrivals and Departures Table
"""
def load_arrivals(request, station):
    arrival_context = get_arrivals(station)
    #print(f'FROM LOAD: {arrival_context}')

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
def update_arrivals_table(request, table_id):
    station = request.POST.get('station', "30th Street Station") 
    arrival_context = get_arrivals(station)
   # print(f'FROM UPDATE: {arrival_context}')
    match table_id:
        case 'tbl_all_arrivals':
            data = arrival_context['all_arrivals_ctx']
        case 'tbl_air_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Airport']
        case 'tbl_che_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Chestnut Hill East']
        case 'tbl_chw_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Chestnut Hill West']
        case 'tbl_lan_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Lansdale/Doylestown']
        case 'tbl_med_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Media/Wawa']
        case 'tbl_fox_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Fox Chase']
        case 'tbl_nor_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Manayunk/Norristown']
        case 'tbl_pao_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Paoli/Thorndale']
        case 'tbl_cyn_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Cynwyd']
        case 'tbl_tre_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Trenton']
        case 'tbl_war_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Warminster']
        case 'tbl_wil_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Wilmington/Newark']
        case 'tbl_wtr_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['West Trenton']

    html = render_to_string('info_board/table_rows.html', {'arrivals' : data})
    return JsonResponse({'html': html})