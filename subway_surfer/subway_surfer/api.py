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
            arrivals_info = []
            
            for key, value in parsed_data.items():
                
                if isinstance(value, list) and not value:
                    continue
                
                for item in value:
                    for direction, arrivals in item.items():
                        #print(f'{bcolors.WARNING}{item.items()}{bcolors.RESET}')
                        for arrival in arrivals:
                            print(f'{bcolors.WARNING}{arrival}{bcolors.RESET}')
                            arrival_info = {
                                "direction": arrival["direction"],
                                "train_id": arrival["train_id"],
                                "origin": arrival["origin"],
                                "destination": arrival["destination"],
                                "line": arrival["line"],
                                "status": arrival["status"],
                                "service_type": arrival["service_type"],
                                "next_station": arrival["next_station"],    
                                "sched_time": arrival["sched_time"],        #TO DO: Format times
                                "depart_time": format_time(arrival["depart_time"]),
                                "track": arrival["track"],
                            }
                            arrivals_info.append(arrival_info)


            context = {
                    'station':station,
                    'arrivals_info': arrivals_info ,
                    'optText': 'Train Information', 
                }
        
            return context
        else:
            return JsonResponse({'error': 'API request failed'}, status=500)
