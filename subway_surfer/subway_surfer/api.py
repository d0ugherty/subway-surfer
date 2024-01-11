import requests
from .bcolors import bcolors
from django.http import JsonResponse
from .utils import format_time
from .models import Trip, Route

"""Make API call to retrieve Arrival information"""
def get_arrivals(station):
        api_url = f'https://www3.septa.org/api/Arrivals/index.php?station={station}'
        response = requests.get(api_url)
        context = {}
        if response.status_code == 200:
            context['station'] = station
            context = process_arrivals_json(response, context)
            return context
        else:
            return JsonResponse({'error': 'API request failed'}, status=500)
    
def process_arrivals_json(response, context):
    all_arrivals = []
    arrivals_by_line = {'Airport' : [], 
                        'Chestnut Hill East' : [],
                        'Chestnut Hill West' : [],
                        'Lansdale/Doylestown': [],
                        'Media/Wawa' : [],
                        'Fox Chase' : [],
                        'Manayunk/Norristown' : [],
                        'Paoli/Thorndale' : [],
                        'Cynwyd' : [],
                        'Trenton' : [],
                        'Warminster' : [],
                        'Wilmington/Newark' : [],
                        'West Trenton' : []
                    }
    parsed_data = response.json()
            #print(f'{bcolors.WARNING}{parsed_data}{bcolors.RESET}') 
            
    for key, value in parsed_data.items():
        
        if isinstance(value, list) and not value:
            continue
        
        for item in value:
            if isinstance(item, dict):
                for direction, next_to_arrive in item.items():
                    #print(f'{bcolors.WARNING}{item.items()}{bcolors.RESET}')
                    for train in next_to_arrive:
                    # print(f'{bcolors.WARNING}{arrival}{bcolors.RESET}')
                        train_info = {
                            "direction": train["direction"],
                            "train_id": train["train_id"],
                            "origin": train["origin"],
                            "destination": train["destination"],
                            "line": train["line"],
                            "status": train["status"],
                            "service_type": train["service_type"],
                            "next_station": train["next_station"],    
                            "sched_time": train["sched_time"], 
                            "depart_time": format_time(train["depart_time"]),
                            "track": train["track"],
                        }
                        #print(train_info)
                        line = train["line"]
                        all_arrivals.append(train_info)
                        arrivals_by_line[line].append(train_info)

                        train_info['route'] = get_route(train_info)

                        if train_info['destination'] == 'Fox Chase' and train_info['line'] == 'Airport':
                            arrivals_by_line['Fox Chase'].append(train_info)
                        if train_info['destination'] == 'Warminster' and train_info['line'] == 'Airport':
                            arrivals_by_line['Warminster'].append(train_info)
                        if train_info['destination'] == 'Airport':
                            arrivals_by_line['Airport'].append(train_info)
            else: 
                pass 

    context = {
        'all_arrivals_ctx' : all_arrivals,
        'arrivals_by_line_ctx' : arrivals_by_line,
        'optText' : 'Train Information'
    }
    return context

def get_route(train_info):
    trips_queryset = Trip.objects.filter(block_id=int(train_info['train_id']))
    print(trips_queryset)
    return 
    
        