from .bcolors import bcolors
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import *
from .models import Stop
from .utils import validate_station_name, parse_time
from .consumer import map_marker_data, get_arrivals, arrivals_by_track
from django.shortcuts import redirect
import datetime


def home(request):
    return render(request, 'home.html')

"""
    Renders the map page elements - map and agency form
"""
def map_page_view(request):
    agency_check = AgencyCheckBox(request.GET or None)
    train_marker_data = map_markers(request, agency='SEPTA')
    show_njt_route = False
    show_septa_route = False
    show_septa_markers = True
    njt_shapes = None
    septa_shapes = None
    
    if request.method == 'GET':
        if agency_check.is_valid():

            show_septa_route = agency_check.cleaned_data['show_septa']
            show_njt_route = agency_check.cleaned_data['show_njt']

            if show_njt_route:
                njt_shapes = Agency.get_agency('NJT').get_shapes()
            if show_septa_route:
                septa_shapes = Agency.get_agency('SEPTA').get_shapes()
            return render(request, 'map.html', {'agency_check' : agency_check,
                                                    'train_marker_data': train_marker_data,
                                                    'njt_shapes' : njt_shapes,
                                                    'septa_shapes': septa_shapes,
                                                    'show_septa_markers' : show_septa_markers})


    return render(request, 'map.html', {'agency_check' : agency_check,
                                        'train_marker_data': train_marker_data,
                                        'njt_shapes' : njt_shapes,
                                        'septa_shapes': septa_shapes,
                                        'show_septa_markers': show_septa_markers})

"""
    Endpoint for the map marker data. Establishing the real-time location data
    as its own endpoint makes it easier to fetch with JavaScript, while the 
    Consumer module handles the backend logic.
"""
def map_markers(request, agency):
    train_data = None
    if request.method == 'GET':
        train_data = map_marker_data(agency)
        return JsonResponse(train_data, safe=True)
    else:
        return JsonResponse({'error': f'Request method {request.method} not supported'}, states=405)


"""
    Renders form and redirects to the train information board

    TO DO: Refactor this to make it work with next to arrive
"""
def train_info(request, template_name='info_board/arrivals.html', redirect_dest='load_arrivals'):
    # default
    station = "30th Street Station"
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

    TO-DO: Error handling or preventing on station == None
"""
def load_arrivals(request, station):
    arrival_context = get_arrivals(station,agency='SEPTA')
    form = StationSlctForm() 
    septa = Agency.get_agency('SEPTA')
    septa_routes = septa.get_routes()
    
    arrivals_data = { 'all_arrivals_ctx': arrival_context['N']['all_arrivals_ctx'][:5] + arrival_context['S']['all_arrivals_ctx'][:5] }
    
    if station == 'Gray 30th Street':
        next_acl_time, next_acl_trip = Stop.get_stop('30TH ST. PHL.').next_departure()
        train_info = {
            "direction": "S",
            "train_id": next_acl_trip.block_id,
            "origin" : "Gray 30th Street",
            "destination": next_acl_trip.trip_headsign,
            "line": next_acl_trip.route_name(),
            "sched_time": str(next_acl_time.departure_time),
            "depart_time": str(next_acl_time.departure_time),
            "track": 2
        }

        arrivals_data['all_arrivals_ctx'].append(train_info)
    
    arrivals_data['all_arrivals_ctx'] = sorted(arrivals_data['all_arrivals_ctx'], key=lambda x: x['depart_time'])
    
    for route in septa_routes:
        north_data = arrival_context['N']['arrivals_by_line_ctx'].get(route.route_long_name, [])
        south_data = arrival_context['S']['arrivals_by_line_ctx'].get(route.route_long_name, [])
        arrivals_data[f'{route.route_id.lower().replace(" ", "_")}_arrivals_ctx'] = north_data + south_data

    # TO-DO: Add NJT data
        
    print(f'todays date {datetime.datetime.today()}')
    print(Stop.get_stop('30TH ST. PHL.').next_departure())
 
    # TO-DO: Add NJT's atlantic city line for 30th street

    return render(request, 'info_board/arrivals.html', {
        **arrivals_data, 
        'station': station,
        'form': form
    })

"""
    Update Arrivals
"""
def update_arrivals_table(request, table_id):
    station = request.POST.get('station', "30th Street Station") 
    arrival_context = get_arrivals(station)
    data = []
    all_arrivals = False # controls which columns appear in the table header
    match table_id:
        case 'tbl_all_arrivals':
            data = arrival_context['N']['all_arrivals_ctx'][:5]
            if station == 'Gray 30th Street':
                next_acl_time, next_acl_trip = Stop.get_stop('30TH ST. PHL.').next_departure()
                train_info = {
                    "direction": "S",
                    "train_id": next_acl_trip.block_id,
                    "origin" : "Gray 30th Street",
                    "destination": next_acl_trip.trip_headsign,
                    "line": next_acl_trip.route_name(),
                    "sched_time": str(next_acl_time.departure_time),
                    "depart_time": str(next_acl_time.departure_time),
                    "track": 2
                }
                arrival_context['S']['all_arrivals_ctx'].append(train_info)
            data  += arrival_context['S']['all_arrivals_ctx'][:5]
            all_arrivals = True

        case 'tbl_air_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Airport Line'] 
            data += arrival_context['S']['arrivals_by_line_ctx']['Airport Line'] 

        case 'tbl_che_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Chestnut Hill East Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Chestnut Hill East Line']
            
        case 'tbl_chw_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Chestnut Hill West Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Chestnut Hill West Line']

        case 'tbl_lan_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Lansdale/Doylestown Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Lansdale/Doylestown Line']

        case 'tbl_med_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Media/Wawa Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Media/Wawa Line']
        
        case 'tbl_fox_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Fox Chase Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Fox Chase Line']

        case 'tbl_nor_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Manayunk/Norristown Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Manayunk/Norristown Line']

        case 'tbl_pao_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Paoli/Thorndale Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Paoli/Thorndale Line']
        
        case 'tbl_cyn_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Cynwyd Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Cynwyd Line']
        
        case 'tbl_tre_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Trenton Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Trenton Line']
        
        case 'tbl_war_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Warminster Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Warminster Line']

        case 'tbl_wil_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['Wilmington/Newark Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['Wilmington/Newark Line']

        case 'tbl_wtr_arrivals':
            data = arrival_context['N']['arrivals_by_line_ctx']['West Trenton Line']
            data += arrival_context['S']['arrivals_by_line_ctx']['West Trenton Line']
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
    fare = Fare.get_fare_obj(origin, destination)
    request.session['fare_id'] = fare.fare_id
    request.session['fare_price'] = fare.price()
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

            trains_by_track = arrivals_by_track(stop_name)
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
    trains_by_track = arrivals_by_track(station)
    return render(request, 'nta/tracks.html', {'trains_by_track': trains_by_track})