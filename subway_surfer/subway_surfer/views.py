from .bcolors import bcolors
from django.shortcuts import render
#from django.http import JsonResponse, HttpResponse
from django.utils.timezone import utc
from .forms import *
from .models import Stop
from .utils import validate_station_name
from .consumer import Consumer
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
    arrival_context = Consumer.get_arrivals(station)
    form = StationSlctForm() 
    return render(request, 'info_board/arrivals.html', {
        'all_arrivals_ctx': arrival_context['all_arrivals_ctx'],
        'air_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Airport Line'],
        'che_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Chestnut Hill East Line'],
        'chw_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Chestnut Hill West Line'],
        'lan_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Lansdale/Doylestown Line'],
        'med_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Media/Wawa Line'],
        'fox_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Fox Chase Line'],
        'nor_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Manayunk/Norristown Line'],
        'pao_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Paoli/Thorndale Line'],
        'cyn_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Cynwyd Line'],
        'tre_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Trenton Line'],
        'war_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Warminster Line'],
        'wil_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['Wilmington/Newark Line'],
        'wtr_arrivals_ctx': arrival_context['arrivals_by_line_ctx']['West Trenton Line'],
        'station': station,
        'form': form 
    })


"""Update Arrivals"""
def update_arrivals_table(request, table_id):
    station = request.POST.get('station', "30th Street Station") 
    arrival_context = Consumer.get_arrivals(station)
    data = []
    all_arrivals = False # controls which columns appear in the table header
    match table_id:
        case 'tbl_all_arrivals':
            data = arrival_context['all_arrivals_ctx']
            all_arrivals = True
        case 'tbl_air_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Airport Line'] 
        case 'tbl_che_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Chestnut Hill East Line']
        case 'tbl_chw_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Chestnut Hill West Line']
        case 'tbl_lan_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Lansdale/Doylestown Line']
        case 'tbl_med_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Media/Wawa Line']
        case 'tbl_fox_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Fox Chase Line']
        case 'tbl_nor_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Manayunk/Norristown Line']
        case 'tbl_pao_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Paoli/Thorndale Line']
        case 'tbl_cyn_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Cynwyd Line']
        case 'tbl_tre_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Trenton Line']
        case 'tbl_war_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Warminster Line']
        case 'tbl_wil_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['Wilmington/Newark Line']
        case 'tbl_wtr_arrivals':
            data = arrival_context['arrivals_by_line_ctx']['West Trenton Line']
    return render(request, 'info_board/table_rows.html', {'arrivals': data, 'all_arrivals': all_arrivals})


"""
    Section for Fare Calculation

"""
def fare_calculator(request):
    agency_form = AgencySlctForm(request.POST or None)
    route_form = None

    if request.method == 'POST' and agency_form.is_valid():
        agency = agency_form.cleaned_data['agency_choice']
        route_form = RouteSlctForm(agency, request.POST or None) 

        if route_form.is_valid():
            print('route form valid')
            
    return render(request, 'fare/fare.html', {
        'agency_slct_form' : agency_form,
        'route_slct_form' : route_form
        })

"""
def select_route(request, agency):
    route_form = RouteSlctForm(agency)
    if request.method == 'POST':
        if route_form.is_valid():
            route = route_form['route_choice']
            return redirect('fare_calculator', { 
                        'agency': agency,
                        'route': route })
        else:
            print(route_form.errors)

    else:
        return render(request, 'fare/fare.html', {
        'route_slct_form' : route_form
        })
"""