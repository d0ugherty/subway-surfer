from datetime import datetime

"""Because some of SEPTA's stop names in the static GTFS data are different from
what their API endpoint expects lol"""
def validate_station_name(station_name):
    match station_name:
        case "Gray 30th Street":
            return "30th Street Station"
        case "49th Street":
            return "49th St"
        case "Airport Terminal E F":
            return "Airport Terminal E-F"
        case "Airport Terminal C D":
            return "Airport Terminal C-D"
        case "Chester":
            return "Chester TC"
        case "9th Street Landsdale":
            return "9th St"
        case "Fort Washington":
            return "Ft Washington"
        case "Norristown - Elm Street":
            return "Elm St"
        case __:
            return str(station_name)

"""Format the departure time to make it more readable"""
def format_time(depart_time):
    depart_time = depart_time[:-4]
    depart_time_dt = datetime.strptime(depart_time, '%Y-%m-%d %H:%M:%S')
    formatted_depart_time = depart_time_dt.strftime('%I:%M %p')
    return formatted_depart_time

def clean_string(s):
    if s is not None:
        return s.strip().rstrip('.')
    else:
        return None

def parse_time(time_str):
    return datetime.strptime(time_str, '%I:%M %p')

def now():
    now = str(datetime.now())
    return datetime.strptime(now,"%H:%M:%S")