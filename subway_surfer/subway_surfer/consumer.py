import requests
from .bcolors import bcolors
from django.http import JsonResponse
from .utils import format_time, clean_string, get_digits
from datetime import datetime, timedelta
from .models import Trip, Route, Stop


class Consumer:
        
    def get_arrivals(station, results=20):
            results = results / 2
            api_url = f'https://www3.septa.org/api/Arrivals/index.php?station={station}&results={results}&direction=N'
            response = requests.get(api_url)
            context = {}
            if response.status_code == 200:
                context['station'] = station
                context = Consumer._process_arrivals_json(response, context)
        
            api_url = f'https://www3.septa.org/api/Arrivals/index.php?station={station}&results={results}&direction=S'
            response = requests.get(api_url)
            if response.status_code == 200:
                context['station'] = station
                context = context | Consumer._process_arrivals_json(response, context)
                return context
            else:
                return JsonResponse({'error': 'API request failed'}, status=500)
    
    def arrivals_by_track(station):
        #initialize
        print(f'STATION: {station}')
        track_numbers = ["1", "2", "3", "4", "5", "6", "8", "9", "10"]
        track_dict = { track: {} for track in track_numbers}

        arrivals = Consumer.get_arrivals(station, results=10)
        for track_number in track_dict:
            for arrival in arrivals['all_arrivals_ctx']:
                arriving_track = get_digits(arrival['track'])
                # get only the next arriving train by short circuiting
                if track_dict[track_number] == {} and track_number == arriving_track:
                    arrival['eta'] = Consumer.countdown(arrival)
                    track_dict[track_number] = arrival
                   # print(Consumer.countdown(arrival))
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

    @staticmethod
    def _process_arrivals_json(response, context):
        all_arrivals = []
        arrivals_by_line = Consumer._initialize_arrivals_by_line()
        parsed_data = response.json()
                
        for key, value in parsed_data.items():
            print(f'key: {key}')
            if isinstance(value, list) and not value:
                continue
            Consumer._process_train_data(value, all_arrivals, arrivals_by_line)

        context = {
            'all_arrivals_ctx' : all_arrivals,
            'arrivals_by_line_ctx' : arrivals_by_line,
            'optText' : 'Train Information'
        }
        return context
    
    @staticmethod
    def _get_route(train_info):
        try:
            trip = Trip.objects.filter(block_id=train_info['train_id']).latest('block_id')
        except Trip.DoesNotExist:
            trip_route = train_info['line'] + ' Line'
            return trip_route
        trip_route = trip.route.route_short_name
        return trip_route
    
    @staticmethod
    def _handle_thru_routing(train_info, arrivals_by_line):
        if train_info['destination'] == 'Fox Chase' and train_info['line'] == 'Airport':
            if train_info not in arrivals_by_line['Fox Chase Line']:
                arrivals_by_line['Fox Chase Line'].append(train_info)
       
        if train_info['destination'] == 'Warminster' and train_info['line'] == 'Airport':
            if train_info not in arrivals_by_line['Warminster Line']:
                arrivals_by_line['Warminster Line'].append(train_info)
        return arrivals_by_line
    
    @staticmethod
    def _initialize_arrivals_by_line():
        return {
                'Airport Line' : [], 
                'Chestnut Hill East Line' : [],
                'Chestnut Hill West Line' : [],
                'Lansdale/Doylestown Line': [],
                'Media/Wawa Line' : [],
                'Fox Chase Line' : [],
                'Manayunk/Norristown Line' : [],
                'Paoli/Thorndale Line' : [],
                'Cynwyd Line' : [],
                'Trenton Line' : [],
                'Warminster Line' : [],
                'Wilmington/Newark Line' : [],
                'West Trenton Line' : []
            }

    @staticmethod
    def _process_train_data(train_data, all_arrivals, arrivals_by_line):
        for item in train_data:
            if not isinstance(item, dict):
                continue
            for next_to_arrive in item.values():
                for train in next_to_arrive:
                    train_info = Consumer._parse_train_info(train)
                    train_info['headsign'] = Consumer._get_headsign(train_info)
                    all_arrivals.append(train_info)
                    Consumer._update_arrivals_by_line(train_info, arrivals_by_line)

    @staticmethod
    def _parse_train_info(train):
        return {
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


    
    @staticmethod
    def _update_arrivals_by_line(train_info, arrivals_by_line):
        route = Consumer._get_route(train_info)
        train_info['headsign'] = Consumer._get_headsign(train_info)

        arrivals_by_line[route].append(train_info)
        arrivals_by_line = Consumer._handle_thru_routing(train_info, arrivals_by_line)

    @staticmethod
    def _get_headsign(train_info):
        try:
            trip = Trip.objects.filter(block_id=train_info['train_id']).latest('block_id')
        except Trip.DoesNotExist:
            return train_info['destination']
        return trip.trip_headsign

