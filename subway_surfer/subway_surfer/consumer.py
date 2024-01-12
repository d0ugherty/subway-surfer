import requests
from .bcolors import bcolors
from django.http import JsonResponse
from .utils import format_time, clean_string
from .models import Trip, Route


class Consumer:
        
    def get_arrivals(station):
            results = 30
            api_url = f'https://www3.septa.org/api/Arrivals/index.php?station={station}&results={results}'
            response = requests.get(api_url)
            context = {}
            if response.status_code == 200:
                context['station'] = station
                context = Consumer._process_arrivals_json(response, context)
                return context
            else:
                return JsonResponse({'error': 'API request failed'}, status=500)
            
    @staticmethod
    def _process_arrivals_json(response, context):
        all_arrivals = []
        arrivals_by_line = Consumer._initialize_arrivals_by_line()
        parsed_data = response.json()
                #print(f'{bcolors.WARNING}{parsed_data}{bcolors.RESET}') 
                
        for key, value in parsed_data.items():
            if isinstance(value, list) and not value:
                continue
            Consumer._process_train_data(value, all_arrivals, arrivals_by_line)


        context = {
            'all_arrivals_ctx' : all_arrivals[:10],
            'arrivals_by_line_ctx' : arrivals_by_line,
            'optText' : 'Train Information'
        }
        return context
    
    @staticmethod
    def _get_route(train_info):
        try:
            trip = Trip.objects.filter(block_id=train_info['train_id']).latest('block_id')
        except Trip.DoesNotExist:
            print(f'Trip {train_info["train_id"]} does not exist.')
            return None
        trip_route = trip.route.route_short_name
        return trip_route
    
    @staticmethod
    def _handle_thru_routing(train_info, arrivals_by_line):
        if train_info['destination'] == 'Fox Chase' and train_info['line'] == 'Airport':
            arrivals_by_line['Fox Chase Line'].append(train_info)
       # if train_info['destination'] == 'Airport' and train_info['']
        if train_info['destination'] == 'Warminster' and train_info['line'] == 'Airport':
            arrivals_by_line['Warminster Line'].append(train_info)
        return arrivals_by_line
    
    @staticmethod
    def _initialize_arrivals_by_line():
        return {'Airport Line' : [], 
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
                'West Trenton Line' : [],
                'Express' : []
            }

    @staticmethod
    def _process_train_data(train_data, all_arrivals, arrivals_by_line):
        for item in train_data:
            if not isinstance(item, dict):
                continue
            for next_to_arrive in item.values():
                for train in next_to_arrive:
                    train_info = Consumer._parse_train_info(train)
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
        arrivals_by_line[route].append(train_info)
        arrivals_by_line = Consumer._handle_thru_routing(train_info, arrivals_by_line)

