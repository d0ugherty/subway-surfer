from .models import Stop
from .utils import convert_twelve_hour

""""""

def get_next_departure(station):
    if station == 'Gray 30th Street':
        njt_stop_name = '30TH ST. PHL.'
    elif station == 'Trenton':
        njt_stop_name = 'TRENTON TRANSIT CENTER'
    else:
        return None
    
    context = { 'station': station, 'N': None, 'S': None }

    next_stop_time, next_trip = Stop.get_stop(njt_stop_name).next_departure()
    
    train_info = _parse_train_info(next_stop_time, next_trip, njt_stop_name)

    context[train_info['direction']] = train_info

    return context

def get_departures(station):
    if station == 'Gray 30th Street':
        njt_stop_name = '30TH ST. PHL.'
    elif station == 'Trenton':
        njt_stop_name = 'TRENTON TRANSIT CENTER'
    else:
        return None
    
    context = {'station': station, 'N': None, 'S': None }

    njt_stop = Stop.get_stop(njt_stop_name)

    #Northbound
    stop_times_n, trips_n = njt_stop.upcoming_departures(0)
    #Southbound
    stop_times_s, trips_s = njt_stop.upcoming_departures(1)

    departing_trains_n = []
    for stop_time, trip in zip(stop_times_n, trips_n):
        train_info =_parse_train_info(stop_time, trip, station)
        departing_trains_n.append(train_info)

    departing_trains_s = []
    for stop_time, trip in zip(stop_times_s, trips_s):
        train_info = _parse_train_info(stop_time, trip, station)
        departing_trains_s.append(train_info)
    
    context['N'] = departing_trains_n
    context['S'] = departing_trains_s
   
    return context

def _parse_train_info(stop_time, trip, station):

    train_info = {
        "agency" : "NJ Transit",
        "direction": 'N' if trip.direction_id == 0 else 'S',
        "train_id": trip.block_id,
        "origin" : station,
        "destination": trip.trip_headsign,
        "line": trip.route_name(),
        "sched_time": convert_twelve_hour(str(stop_time.departure_time)),
        "depart_time": convert_twelve_hour(str(stop_time.departure_time)),
        "track": ""
    }
        

    return train_info