from .models import *
from .utils import convert_twelve_hour

""""""

def get_njt_info(station):
    if station == 'Gray 30th Street':
        njt_stop = '30TH ST. PHL.'

    elif station == 'Trenton':
        njt_stop = 'TRENTON TRANSIT CENTER'
    
    else:
        return None
    
    next_stop_time, next_trip = Stop.get_stop(njt_stop).next_departure()
    
    train_info = {
        "direction": 'N' if next_trip.direction_id == 0 else 'S',
        "train_id": next_trip.block_id,
        "origin" : station,
        "destination": next_trip.trip_headsign,
        "line": next_trip.route_name(),
        "sched_time": convert_twelve_hour(str(next_stop_time.departure_time)),
        "depart_time": convert_twelve_hour(str(next_stop_time.departure_time)),
        "track": ""
    }

    return train_info
