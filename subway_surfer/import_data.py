
from subway_surfer.wsgi import *
from subway_surfer.models import *
import os
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
    print('Clearing shape data...')
    Shape.objects.all().delete()
    

def import_stop_data(csv_file_path):
    print("Importing stops...")
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Stop.objects.create(
                stop_id=row['stop_id'].strip(),
                stop_name=row['stop_name'].strip(),
                stop_desc=row['stop_desc'].strip(),
                stop_lat=row['stop_lat'].strip(),
                stop_lon=row['stop_lon'].strip(),
                zone_id=row['zone_id'].strip(),
                **({'stop_url': row['stop_url'].strip()} if 'stop_url' in row else {})
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
                agency_id = row['agency_id'].strip(),
                agency_name = row['agency_name'].strip(),
                agency_url = row['agency_url'].strip(),
                agency_timezone = row['agency_timezone'].strip(),
                agency_lang = row['agency_lang'].strip(),
                **({'agency_email': row['agency_email'].strip()} if 'agency_email' in row else {})
            )

def import_route_data(file_path):
    print("Importing routes...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Route.objects.create(
                route_id=row['route_id'].strip(),
                route_short_name=row['route_short_name'].strip(),
                route_long_name=row['route_long_name'].strip(),
                **({'route_desc': row['route_desc'].strip()} if 'route_desc' in row else {}),
                agency = Agency.objects.get(agency_id=row['agency_id'].strip()),
                route_type=row['route_type'].strip(),
                **({'route_color': row['route_color'].strip()} if 'route_color' in row else {}),
                **({'route_text_color': row['route_text_color'].strip()} if 'route_text_color' in row else {}),
                **({'route_url': row['route_url'].strip()} if 'route_url' in row else {})

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
                fare_id = row['fare_id'].strip(),
                origin_id = row['origin_id'].strip(),
                destination_id = row['destination_id'].strip()
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
                fare = Fare.objects.get(fare_id=row['fare_id'].strip()),
                price = row['price'].strip(),
                currency_type = row['currency_type'].strip(),
                payment_method = row['payment_method'].strip(),
                transfers = row['transfers'].strip(),
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
                route = Route.objects.get(route_id=row['route_id'].strip()),
                service_id = row['service_id'].strip(),
                trip_id = row['trip_id'].strip(),
                trip_headsign = row['trip_headsign'].strip(),
                block_id = row['block_id'].strip(),
                **({'trip_short_name': row['trip_short_name'].strip()} if 'trip_short_name' in row else {}),
                shape_id = row['shape_id'].strip(),
                direction_id = row['direction_id'].strip()
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
                trip = Trip.objects.get(trip_id=row['trip_id'].strip()),
                arrival_time = row['arrival_time'].strip(),
                departure_time = row['departure_time'].strip(),
                stop = Stop.objects.get(stop_id=row['stop_id'].strip()),
                stop_sequence = row['stop_sequence'].strip(),
                pickup_type = row['pickup_type'].strip(),
                drop_off_type = row['drop_off_type'].strip()
            )

def import_shape_data(file_path):
    print("Importing shape data...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Shape.objects.create(
                shape_id = row['shape_id'].strip(),
                shape_pt_lat = row['shape_pt_lat'].strip(),
                shape_pt_lon = row['shape_pt_lon'].strip(),
                shape_pt_sequence = row['shape_pt_sequence'].strip(),
                **({'shape_dist_traveled': row['shape_dist_traveled'].strip()} if 'shape_dist_traveled' in row else {})
            )

def import_calendar_date(file_path):
    print("Importing calendar dates...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1
            print(f'{" " * 20}Importing row {i}', end='\r')
            Calendar_Date.objects.create(
                service_id = row['service_id'].strip(),
                date = row['date'].strip(),
                exception_type = row['exception_type'].strip()
            )

def import_calendar(file_path):
    print("Importing calendar data...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
            i += 1 
            print(f'{" " * 20}Importing row {i}', end='\r')
            Calendar.objects.create(
                service_id = row['service_id'].strip(),
                monday = row['monday'].strip(),
                tuesday = row['tuesday'].strip(),
                wednesday = row['wednesday'].strip(),
                thursday = row['thursday'].strip(),
                friday = row['friday'].strip(),
                start_date = row['start_date'].strip(),
                end_date = row['end_date'].strip()
            )
        
if __name__ == '__main__':
    clear_existing_data()
    agencies = ['septa', 'njt']
    for agency in agencies:
        print(f'Importing data for {agency}..')
        import_agency_data(f'data/{agency}/agency.csv')
        print("[1/10] \n\n")
        import_stop_data(f'data/{agency}/stops.csv')
        print("[2/10]\n")
        import_route_data(f'data/{agency}/routes.csv')
        print("[3/10]\n")

        if os.path.exists(f'data/{agency}/fare_rules.csv'):
            import_fare_data(f'data/{agency}/fare_rules.csv')
        else:
            print(f"File data/{agency}/fare_rules.csv does not exist.")
        print("[4/10]\n")

        if os.path.exists(f'data/{agency}/fare_attributes.csv'):
            import_fare_attributes(f'data/{agency}/fare_attributes.csv')
        else:
            print(f"File data/{agency}/fare_attributes.csv does not exist.")
        print("[5/10]\n")

        import_shape_data(f'data/{agency}/shapes.csv')
        print("[6/10]\n")
    
        import_trip_data(f'data/{agency}/trips.csv')
        print("[7/10]\n")
        import_stop_time_data(f'data/{agency}/stop_times.csv')
        print("[8/10]\n")
        import_calendar_date(f'data/{agency}/calendar_dates.csv')
        print("[9/10]")

        if os.path.exists(f'data/{agency}/calendar.csv'):
            import_calendar(f'data/{agency}/calendar.csv')
        else:
            print(f'data/{agency}/calendar.csv does not exist.')
        print("10/10")
        print("Importing complete.")
    