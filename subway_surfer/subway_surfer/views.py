from .bcolors import bcolors
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import *
from .models import Stop
from subway_surfer import utils as  utils
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

            return render(request, 'map.html', {
                'agency_check' : agency_check,
                'train_marker_data': train_marker_data,
                'njt_shapes' : njt_shapes,
                'septa_shapes': septa_shapes,
                'show_septa_markers' : show_septa_markers})


    return render(request, 'map.html', {
        'agency_check' : agency_check,
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

    if request.method == 'GET':
        form = StationSlctForm(request.GET)

        if form.is_valid():
            selected_stop = form.cleaned_data['stop_choice']
            stop_name = utils.validate_station_name(selected_stop)
            # Redirect to the load_arrivals view with the selected stop_name
            return redirect(redirect_dest, station=stop_name)
        
    else:
        form = StationSlctForm()

    context = {'stop_form': form, 'station': station}
    return render(request, template_name, context)

"""
    Render the Arrivals and Departures Table

    TO-DO: 
        Error handling or preventing on station == None
"""
def load_arrivals(request, station):
    septa_context = SEPTA.get_arrivals(station,agency='SEPTA')
    njt_context = NJ_Transit.get_departures(station)
    form = StationSlctForm() 
    route_ids = []
    septa_routes = Agency.get_agency('SEPTA').get_routes()

    septa_arrivals_data = { 'all_arrivals_ctx': septa_context['N']['all_arrivals_ctx'][:5] + septa_context['S']['all_arrivals_ctx'][:5] }

    if njt_context is not None:
        if len(njt_context['N']) > 0 or len(njt_context['S']) > 0:

            njt_arrivals_data = {
                'all_arrivals_ctx' : [njt_context[key] for key in ['N','S'] if njt_context.get(key)]
            }

            all_arrivals = { 'all_arrivals_ctx' : njt_arrivals_data['all_arrivals_ctx'][0] }
            all_arrivals['all_arrivals_ctx'] += septa_arrivals_data['all_arrivals_ctx'] 
            
            all_arrivals['all_arrivals_ctx'] = utils.sort_by_time(all_arrivals['all_arrivals_ctx'])
            all_arrivals['all_arrivals_ctx'] = all_arrivals['all_arrivals_ctx'][:10]
    else:
        all_arrivals = { 'all_arrivals_ctx' : utils.sort_by_time(septa_arrivals_data['all_arrivals_ctx'])}
    
    # For displaying arrivals/departures for SEPTA routes that service the station
    for route in septa_routes:

        north_data = septa_context['N']['arrivals_by_line_ctx'].get(route.route_long_name, [])
        south_data = septa_context['S']['arrivals_by_line_ctx'].get(route.route_long_name, [])

        route_id = route.route_id.lower()
        route_ids.append(route_id)

        route_name_ctx = f'{route_id.replace(" ", "_")}_arrivals_ctx'

        all_arrivals[route_name_ctx] = north_data + south_data
        all_arrivals[route_name_ctx] = utils.sort_by_time(all_arrivals[route_name_ctx])
        all_arrivals[route_name_ctx] = all_arrivals[route_name_ctx][:4]

    route_templates = [
        {'template_name': f'info_board/routes/septa_{id}.html', 'id_arrivals_ctx': f'{id}_arrivals_context'} 
        for id in route_ids
    ]

    return render(request, 'info_board/arrivals.html', {
        **all_arrivals,
        'route_templates': route_templates , 
        'station': station,
        'form': form
    })

"""
    Update Arrivals
"""
def update_arrivals_table(request, table_id, agency='septa'):
    station = request.GET.get('station', "30th Street Station") 
    septa_context = SEPTA.get_arrivals(station)
    njt_context = NJ_Transit.get_departures(station)
    arrivals = []
    show_all_arrivals = False
    route_id = utils.extract_route_id(table_id)
    
    if route_id == 'ALL':
        septa_data = { 'all_arrivals_ctx': septa_context['N']['all_arrivals_ctx'][:5] + septa_context['S']['all_arrivals_ctx'][:5] }
        
        if njt_context is not None:
            if len(njt_context['N']) > 0 or len(njt_context['S']) > 0:

                njt_data = {
                    'all_arrivals_ctx' : [njt_context[key] for key in ['N','S'] if njt_context.get(key)]
                }

                all_arrivals = { 'all_arrivals_ctx' : njt_data['all_arrivals_ctx'][0] }
                all_arrivals['all_arrivals_ctx'] += septa_data['all_arrivals_ctx']

        else:
            all_arrivals = { 'all_arrivals_ctx' : septa_data['all_arrivals_ctx'] }

        all_arrivals['all_arrivals_ctx'] = utils.sort_by_time(all_arrivals['all_arrivals_ctx'])
        arrivals = all_arrivals['all_arrivals_ctx'][:10]
        
        show_all_arrivals = True

    else:
        route_name = Route.get_route(route_id).route_long_name

        arrivals = septa_context['N']['arrivals_by_line_ctx'][route_name]
        arrivals += septa_context['S']['arrivals_by_line_ctx'][route_name]
        arrivals = utils.sort_by_time(arrivals)
        arrivals = arrivals[:4]

        
    return render(request, 'info_board/table_rows.html', {'arrivals': arrivals, 
                                                          'show_all_arrivals': show_all_arrivals, 
                                                          'route_id': route_id.lower()})


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

    if request.method == 'GET':
        form = StationSlctForm(request.GET)

        if form.is_valid():

            selected_stop = form.cleaned_data['stop_choice']
            stop_name = utils.validate_station_name(selected_stop)

            trains_by_track = SEPTA.arrivals_by_track(stop_name)

            return render(request, 'nta/nta.html', { 
                'stop_form' : form,
                'station': stop_name,
                'trains_by_track': trains_by_track
                })
    else:
        form = StationSlctForm()

    context = {'stop_form': form, 'stops': stops, 'station': station}
    return render(request, 'nta/nta.html', context)

def update_next_to_arrive(request, station):
    station = request.GET.get('station', "30th Street Station") 
    trains_by_track = SEPTA.arrivals_by_track(station)
    return render(request, 'nta/tracks.html', {'trains_by_track': trains_by_track})