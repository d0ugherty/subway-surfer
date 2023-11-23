
from rail_surfer.wsgi import *
from rail_surfer.models import Stop, Route, Shape
import csv

def clear_existing_data():
    Stop.objects.all().delete()
    Route.objects.all().delete()
    Shape.objects.all().delete()

def import_stop_data(csv_file_path):
    print("Importing Regional Rail stops...")
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Stop.objects.create(
                stop_id=row['stop_id'],
                stop_name=row['stop_name'],
                stop_desc=row['stop_desc'],
                stop_lat=row['stop_lat'],
                stop_lon=row['stop_lon'],
                zone_id=row['zone_id'],
                stop_url=row['stop_url']
            )

def import_route_data(file_path):
    print("Importing Regional Rail routes...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Route.objects.create(
                route_id=row['route_id'],
                route_short_name=row['route_short_name'],
                route_long_name=row['route_long_name'],
                route_desc=row['route_desc'],
                agency_id=row['agency_id'],
                route_type=row['route_type'],
                route_color=row['route_color'],
                route_text_color=row['route_text_color'],
                route_url=row['route_url']
            )

def import_shape_data(file_path):
    print("Importing Regional Rail shape data...")
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Shape.objects.create(
                shape_id=row['shape_id'],
                shape_pt_lat=row['shape_pt_lat'],
                shape_pt_lon=row['shape_pt_lon'],
                shape_pt_sequence=row['shape_pt_sequence']
            )

if __name__ == '__main__':
   # clear_existing_data()
    import_stop_data('data/stops.csv')
    import_route_data('data/routes.csv')
    import_shape_data('data/shapes.csv')