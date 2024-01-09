import requests
from .bcolors import bcolors
from django.http import JsonResponse
from .utils import format_time

"""Make API call to retrieve Arrival information"""
def get_arrivals(station):
        api_url = f'https://www3.septa.org/api/Arrivals/index.php?station={station}'
        response = requests.get(api_url)
        context = {}
        if response.status_code == 200:
            parsed_data = response.json()
            #print(f'{bcolors.WARNING}{parsed_data}{bcolors.RESET}') 
            arrivals = []
            
            for key, value in parsed_data.items():
                
                if isinstance(value, list) and not value:
                    continue
                
                for item in value:
                    for direction, trains in item.items():
                        #print(f'{bcolors.WARNING}{item.items()}{bcolors.RESET}')
                        for train in trains:
                            print(f'{bcolors.WARNING}{train}{bcolors.RESET}')
                            train_info = {
                                "direction": train["direction"],
                                "train_id": train["train_id"],
                                "origin": train["origin"],
                                "destination": train["destination"],
                                "line": train["line"],
                                "status": train["status"],
                                "service_type": train["service_type"],
                                "next_station": train["next_station"],    
                                "sched_time": train["sched_time"],        #TO DO: Format times
                                "depart_time": format_time(train["depart_time"]),
                                "track": train["track"],
                            }
                            arrivals.append(train_info)


            context = {
                    'station':station,
                    'arrivals': arrivals ,
                    'optText': 'Train Information', 
                }
        
            return context
        else:
            return JsonResponse({'error': 'API request failed'}, status=500)
