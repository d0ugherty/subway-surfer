import requests
from .bcolors import bcolors
from django.http import JsonResponse
from .utils import format_time, clean_string, get_digits
from datetime import datetime
from .models import Trip, Agency

def get_arrivals(station, results=50,agency='SEPTA', by_track=False):
        septa_base_url = f'https://www3.septa.org/api/Arrivals/index.php?station={station}'

        if by_track:
            api_url = f'{septa_base_url}&results={results}'
            response = requests.get(api_url)
            context = { 'station' : station }

            if response.status_code == 200:
                context = _process_arrivals_json(response,context, agency)
                return context
            else:
                return JsonResponse({'error': 'API request failed'}, status=500)
            
        else:

            results = results / 2
            api_url = f'{septa_base_url}&results={results}&direction=N'
            response = requests.get(api_url)
            context = {'station': station, 'N': None, 'S': None}

            if response.status_code == 200:
                context['N'] = _process_arrivals_json(response, context, agency)
        
            api_url = f'{septa_base_url}&results={results}&direction=S'
            response = requests.get(api_url)

            if response.status_code == 200:
                context['S'] = context | _process_arrivals_json(response, context, agency)
            else:
                return JsonResponse({'error': 'API request failed'}, status=500)
        return context

def arrivals_by_track(station):
    #initialize
    track_numbers = ["1", "2", "3", "4", "5", "6", "8", "9", "10"]
    track_dict = { track: {} for track in track_numbers}
    arrivals = get_arrivals(station, results=10, by_track=True)

    for track_number in track_dict:

        for arrival in arrivals['all_arrivals_ctx']:
            
            arriving_track = get_digits(arrival['track'])
    
            if track_dict[track_number] == {} and track_number == arriving_track:
                arrival['eta'] = countdown(arrival)
                track_dict[track_number] = arrival
                
    return track_dict

"""
    Calculates the ETA for an arriving train
"""
def countdown(train_info):
    sched_time = datetime.strptime(train_info['sched_time'], '%Y-%m-%d %H:%M:%S.%f')

    if train_info['status'] != 'On Time':
        min_late = int(get_digits(train_info['status'])) 

    else:
        min_late = 0

    diff = sched_time - datetime.now() 
    return (int(diff.total_seconds()/60) + min_late)

def map_marker_data(agency):
    if agency == 'SEPTA':

        api_url = 'https://www3.septa.org/api/TrainView/index.php'
        response = requests.get(api_url) 
        train_info = {}

        if response.status_code == 200:
            data = response.json()

            for item in data:
                    
                    trainno = item['trainno']
                    train_info[trainno] = {
                        'agency' : agency, 
                        "lat": item['lat'],
                        "lon": item['lon'],
                        "trainno": trainno,
                        "service": item['service'],
                        "dest": item['dest'],
                        "currentstop": item['currentstop'],
                        "nextstop": item['nextstop'],
                        "line": item['line'],
                        "consist": item['consist'],
                        "heading": item['heading'],
                        "late": item['late'],
                        "SOURCE": item['SOURCE'],
                        "TRACK": item['TRACK'],
                        "TRACK_CHANGE": item['TRACK_CHANGE']
                    }
        return train_info


def _process_arrivals_json(response, context, agency_id):
    all_arrivals = []
    agency_routes = Agency.get_agency(agency_id).get_routes()
    arrivals_by_line = { route.route_short_name : [] for route in agency_routes }
    parsed_data = response.json()
            
    for key, value in parsed_data.items():

        if isinstance(value, list) and not value:
            continue
        
        _process_train_data(value, all_arrivals, arrivals_by_line)

    context = {
        'all_arrivals_ctx' : all_arrivals,
        'arrivals_by_line_ctx' : arrivals_by_line,
        'optText' : 'Train Information'
    }
    return context


def _get_route(train_info):
    trip = Trip.get_trip(train_info['train_id'])
    
    if trip == None:
        trip_route = train_info['line'] + ' Line'
        return trip_route
    
    else:
        trip_route = trip.route_name()
        return trip_route


def _process_train_data(train_data, all_arrivals, arrivals_by_line):
    for item in train_data:

        if not isinstance(item, dict):
            continue

        for next_to_arrive in item.values():

            for train in next_to_arrive:

                train_info = _parse_train_info(train)
                train_info['headsign'] = _get_headsign(train_info)
                all_arrivals.append(train_info)
                _update_arrivals_by_line(train_info, arrivals_by_line)


def _parse_train_info(train):
    return {
        "agency" : "SEPTA",
        "direction": clean_string(train["direction"]),
        "train_id": clean_string(train["train_id"]),
        "origin": clean_string(train["origin"]),
        "destination": clean_string(train["destination"]),
        "line": clean_string(train["line"]),
        "status": clean_string(train["status"]),
        "service_type": clean_string(train["service_type"]),
        "next_station": clean_string(train["next_station"]),
        "sched_time": clean_string(train["sched_time"]),
        "depart_time": format_time(clean_string(train["depart_time"])),
        "track": clean_string(train["track"])
        }

def _update_arrivals_by_line(train_info, arrivals_by_line, agency='SEPTA'):
    route = _get_route(train_info)
    train_info['headsign'] = _get_headsign(train_info)

    arrivals_by_line[route].append(train_info)

    if agency == 'SEPTA':
        arrivals_by_line = _handle_thru_routing(train_info, arrivals_by_line)

"""
    Trains from the Airport are typically terminate at Warminster or Fox Chase 
    via Center City
"""
def _handle_thru_routing(train_info, arrivals_by_line):
    if train_info['destination'] == 'Fox Chase' and train_info['line'] == 'Airport':

        if train_info not in arrivals_by_line['Fox Chase Line']:

            arrivals_by_line['Fox Chase Line'].append(train_info)
    
    if train_info['destination'] == 'Warminster' and train_info['line'] == 'Airport':

        if train_info not in arrivals_by_line['Warminster Line']:

            arrivals_by_line['Warminster Line'].append(train_info)

    return arrivals_by_line

def _get_headsign(train_info):
    trip = Trip.get_trip(train_info['train_id'])
    if trip == None:
        return train_info['destination']
    else:
        return trip.trip_headsign
    