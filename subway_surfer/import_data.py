
from subway_surfer.wsgi import *
from subway_surfer.models import *
import csv

def clear_existing_data():
    print('Clearing stop data...')
    Stop.objects.all().delete()
    print('Clearing route data...')
    Route.objects.all().delete()
    print('Clearing agency data...')
    Agency.objects.all().delete()
    print('Clearing fare zone data')
    Fare.objects.all().delete()
    print('Clearing fare zone attributes')
    Fare_Attributes.objects.all().delete()
    print('Clearing trip data...')
    Trip.objects.all().delete()
    print('Clearing stop times...')
    Stop_Time.objects.all().delete()
    #print('Clearing shape data...')
    #Shape.objects.all().delete()

def import_stop_data(csv_file_path):
    print("Importing Regional Rail stops...")
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Stop.objects.create(
                stop_id=row['stop_id'],
                stop_name=row['stop_name'],
                stop_desc=row['stop_desc'],
                stop_lat=row['stop_lat'],
                stop_lon=row['stop_lon'],
                zone_id=row['zone_id'],
                stop_url=row['stop_url']
            )

def import_agency_data(file_path):
    print("Importing agency data...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Agency.objects.create(
                agency_id = row['agency_id'],
                agency_name = row['agency_name'],
                agency_url = row['agency_url'],
                agency_timezone = row['agency_timezone'],
                agency_lang = row['agency_lang'],
                agency_email = row ['agency_email']
            )

def import_route_data(file_path):
    print("Importing Regional Rail routes...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Route.objects.create(
                route_id=row['route_id'],
                route_short_name=row['route_short_name'],
                route_long_name=row['route_long_name'],
                route_desc=row['route_desc'],
                agency = Agency.objects.get(agency_id=row['agency_id']),
                route_type=row['route_type'],
                route_color=row['route_color'],
                route_text_color=row['route_text_color'],
                route_url=row['route_url']
            )

def import_fare_data(file_path):
    print("Importing fare data...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Fare.objects.create(
                fare_id = row['fare_id'],
                origin_id = row['origin_id'],
                destination_id = row['destination_id']
            )

def import_fare_attributes(file_path):
    print("Importing fare attributes...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Fare_Attributes.objects.create(
                fare = Fare.objects.get(fare_id=row['fare_id']),
                price = row['price'],
                currency_type = row['currency_type'],
                payment_method = row['payment_method'],
                transfers = row['transfers'],
                transfer_duration = row['transfer_duration'].strip()
            )

def import_trip_data(file_path):
    print("Importing trip data...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Trip.objects.create(
                route = Route.objects.get(route_id=row['route_id']),
                service_id = row['service_id'],
                trip_id = row['trip_id'],
                trip_headsign = row['trip_headsign'],
                block_id = row['block_id'],
                trip_short_name = row['trip_short_name'],
                shape_id = row['shape_id'],
                direction_id = row['direction_id']
            )

def import_stop_time_data(file_path):
    print("Importing stop time data...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Stop_Time.objects.create(
                trip = Trip.objects.get(trip_id=row['trip_id']),
                arrival_time = row['arrival_time'],
                departure_time = row['departure_time'],
                stop = Stop.objects.get(stop_id=row['stop_id']),
                stop_sequence = row['stop_sequence'],
                pickup_type = row['pickup_type'],
                drop_off_type = row['drop_off_type']
            )

def import_shape_data(file_path):
    print("Importing Regional Rail shape data...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Shape.objects.create(
                shape_id=row['shape_id'],
                shape_pt_lat=row['shape_pt_lat'],
                shape_pt_lon=row['shape_pt_lon'],
                shape_pt_sequence=row['shape_pt_sequence']
            )

if __name__ == '__main__':
    clear_existing_data()
    import_agency_data('data/agency.csv')
    print("[1/8] \n\n")
    import_stop_data('data/stops.csv')
    print("[2/8]\n")
    import_route_data('data/routes.csv')
    print("[3/8]\n")
    import_fare_data('data/fare_rules.csv')
    print("[4/8]\n")
    import_fare_attributes('data/fare_attributes.csv')
    print("[5/8]\n")
    #import_shape_data('data/shapes.csv')
    print("[6/8]\n")
    import_trip_data('data/trips.csv')
    print("[7/8]\n")
    import_stop_time_data('data/stop_times.csv')
    print("[8/8]\n")
    print("Importing complete.")