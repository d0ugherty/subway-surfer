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
    return render(request, 'home.html')

"""
    Renders form and redirects to the train information board

    TO DO: Refactor this to make it work with next to arrive
"""
def train_info(request, template_name='info_board/arrivals.html', redirect_dest='load_arrivals'):
    # default
    station = "30th Street Station"
    #print(request.method)
    if request.method == 'POST':
        form = StationSlctForm(request.POST)
        if form.is_valid():
            selected_stop = form.cleaned_data['stop_choice']
            stop_name = validate_station_name(selected_stop)
            # Redirect to the load_arrivals view with the selected stop_name
            return redirect(redirect_dest, station=stop_name)
    else:
        form = StationSlctForm()

    stops = Stop.objects.all()
    context = {'stop_form': form, 'stops': stops, 'station': station}
    return render(request, template_name, context)

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
    origin_form = None
    dest_form = None
    price = 0.0

    if request.method == 'POST':
        form_type = request.POST.get('form_type', None)
        
        if form_type == 'agency' and agency_form.is_valid():
            agency = agency_form.cleaned_data['agency_choice']
            request.session['agency_choice'] = agency.id
            route_form = RouteSlctForm(agency)
        
        # Route selection isn't really being used for anything
        # TO DO: Figure out what i should do with it 
        elif form_type == 'route':
            agency_id = request.session.get('agency_choice')
            route_form = RouteSlctForm(agency_id, request.POST)
            if route_form.is_valid():
                origin_form = OriginForm()
            else:
                print(route_form.errors)
            
        elif form_type == 'origin':
            origin_form = OriginForm(request.POST)
            if origin_form.is_valid():
                origin = origin_form.cleaned_data['origin_choice']
                request.session['origin_choice'] = origin.stop_id
                request.session['origin_zone'] = origin.zone_id
                dest_form = DestForm(origin.stop_id)
        
        elif form_type == 'destination':
            dest_form = DestForm(request.session['origin_choice'], request.POST)
            if dest_form.is_valid():
                destination = dest_form.cleaned_data['stops']
                dest_zone = destination.zone_id
                origin_zone = request.session['origin_zone']

                price = get_fare(request, origin_zone, dest_zone)
                

    return render(request, 'fare/fare.html', {
        'agency_slct_form': agency_form,
        'route_slct_form': route_form,
        'origin_form': origin_form,
        'dest_form' : dest_form,
        'price': '${:,.2f}'.format(price)
    })

def get_fare(request, origin, destination):
    fare = Fare.objects.get(origin_id=origin, destination_id=destination)
    request.session['fare_id'] = fare.fare_id
    fare_attributes = Fare_Attributes.objects.get(fare=fare)
    request.session['fare_price'] = fare_attributes.price
    return request.session['fare_price']


"""
    Emulates an information board you'd find on a station platform
    - i should display information by track number
    - What train is next?
    - Distance or time to next train
    - Destination
    - Via
    - Current time
"""
def next_to_arrive(request, station):
    stops = Stop.objects.all()
    if request.method == 'POST':
        form = StationSlctForm(request.POST)
        if form.is_valid():
            selected_stop = form.cleaned_data['stop_choice']
            stop_name = validate_station_name(selected_stop)

            trains_by_track = Consumer.arrivals_by_track(stop_name)
            return render(request, 'nta/nta.html', { 'stop_form' : form,
                                                    'station': stop_name,
                                                    'trains_by_track': trains_by_track
                                                    })
    else:
        form = StationSlctForm()

    context = {'stop_form': form, 'stops': stops, 'station': station}
    return render(request, 'nta/nta.html', context)

def update_next_to_arrive(request, station):
    station = request.POST.get('station', "30th Street Station") 
    trains_by_track = Consumer.arrivals_by_track(station)
    return render(request, 'nta/tracks.html', {'trains_by_track': trains_by_track})