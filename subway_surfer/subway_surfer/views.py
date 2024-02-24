from .bcolors import bcolors
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import *
from .models import Stop
from .utils import validate_station_name
from subway_surfer import septa as SEPTA
from django.shortcuts import redirect
from subway_surfer import nj_transit as NJ_Transit


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
        train_data = SEPTA.map_marker_data(agency)
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
    context = {'stop_form': form, 'station': station}
    return render(request, template_name, context)

"""
    Render the Arrivals and Departures Table

    TO-DO: 
        Error handling or preventing on station == None
        Display multiple NJT departures according to departure time
"""
def load_arrivals(request, station):
    septa_context = SEPTA.get_arrivals(station,agency='SEPTA')
    form = StationSlctForm() 
    septa_routes = Agency.get_agency('SEPTA').get_routes() 
    njt_context = NJ_Transit.get_next_departure(station)

    all_arrivals = {'all_arrivals_ctx': None }

    # combine northbound + southbound arrivals
    septa_arrivals_data = { 'all_arrivals_ctx': septa_context['N']['all_arrivals_ctx'][:5] + septa_context['S']['all_arrivals_ctx'][:5] }
    
    if njt_context is not None:
        njt_arrivals_data = {
            'all_arrivals_ctx' : [njt_context[key] for key in ['N','S'] if njt_context.get(key)]
        }
        
        all_arrivals['all_arrivals_ctx'] = njt_arrivals_data['all_arrivals_ctx'] + septa_arrivals_data['all_arrivals_ctx']
        all_arrivals['all_arrivals_ctx'] = sorted(all_arrivals['all_arrivals_ctx'], key=lambda arrival: arrival['depart_time'])
    else:
        all_arrivals['all_arrivals_ctx'] = sorted(septa_arrivals_data['all_arrivals_ctx'], key=lambda arrival: arrival['depart_time'])
    
    # For displaying arrivals/departures for SEPTA routes that service the station
    # Could do the same for NJT eventually
    for route in septa_routes:

        north_data = septa_context['N']['arrivals_by_line_ctx'].get(route.route_long_name, [])
        south_data = septa_context['S']['arrivals_by_line_ctx'].get(route.route_long_name, [])
        all_arrivals[f'{route.route_id.lower().replace(" ", "_")}_arrivals_ctx'] = north_data + south_data

    return render(request, 'info_board/arrivals.html', {
        **all_arrivals, 
        'station': station,
        'form': form
    })

"""
    Update Arrivals
"""
def update_arrivals_table(request, table_id):
    station = request.POST.get('station', "30th Street Station") 
    septa_context = SEPTA.get_arrivals(station)
    njt_context = NJ_Transit.get_next_departure(station)
    data = []
    show_all_arrivals = False # controls which columns appear in the table header

    match table_id:

        case 'tbl_all_arrivals':

            septa_data = { 'all_arrivals_ctx': septa_context['N']['all_arrivals_ctx'][:5] + septa_context['S']['all_arrivals_ctx'][:5] }

            if njt_context is not None:
                njt_data = {
                    'all_arrivals_ctx' : [njt_context[key] for key in ['N','S'] if njt_context.get(key)]
                }

            all_arrivals = {'all_arrivals_ctx': None }
            all_arrivals['all_arrivals_ctx'] = njt_data['all_arrivals_ctx'] + septa_data['all_arrivals_ctx']
            all_arrivals['all_arrivals_ctx'] = sorted(all_arrivals['all_arrivals_ctx'], key=lambda arrival: arrival['depart_time'])

            data = all_arrivals['all_arrivals_ctx']

        case 'tbl_air_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Airport Line'] 
            data += septa_context['S']['arrivals_by_line_ctx']['Airport Line'] 

        case 'tbl_che_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Chestnut Hill East Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Chestnut Hill East Line']
            
        case 'tbl_chw_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Chestnut Hill West Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Chestnut Hill West Line']

        case 'tbl_lan_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Lansdale/Doylestown Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Lansdale/Doylestown Line']

        case 'tbl_med_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Media/Wawa Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Media/Wawa Line']
        
        case 'tbl_fox_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Fox Chase Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Fox Chase Line']

        case 'tbl_nor_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Manayunk/Norristown Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Manayunk/Norristown Line']

        case 'tbl_pao_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Paoli/Thorndale Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Paoli/Thorndale Line']
        
        case 'tbl_cyn_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Cynwyd Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Cynwyd Line']
        
        case 'tbl_tre_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Trenton Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Trenton Line']
        
        case 'tbl_war_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Warminster Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Warminster Line']

        case 'tbl_wil_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['Wilmington/Newark Line']
            data += septa_context['S']['arrivals_by_line_ctx']['Wilmington/Newark Line']

        case 'tbl_wtr_arrivals':
            data = septa_context['N']['arrivals_by_line_ctx']['West Trenton Line']
            data += septa_context['S']['arrivals_by_line_ctx']['West Trenton Line']

    return render(request, 'info_board/table_rows.html', {'arrivals': data, 'show_all_arrivals': show_all_arrivals})


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

            trains_by_track = SEPTA.arrivals_by_track(stop_name)

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
    trains_by_track = SEPTA.arrivals_by_track(station)
    return render(request, 'nta/tracks.html', {'trains_by_track': trains_by_track})