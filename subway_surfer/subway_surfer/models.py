from django.db import models


"""
    Options for station selection menu and map locations
"""
class Stop(models.Model):
    stop_id = models.IntegerField()
    stop_name = models.CharField(max_length=100)
    stop_desc = models.CharField(max_length=100)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    zone_id = models.CharField(max_length=10)
    stop_url = models.CharField(max_length=100)

    def __str__(self):
        return self.stop_name
    
class Agency(models.Model):
    agency_id = models.CharField(max_length=25)
    agency_name = models.CharField(max_length=50)
    agency_url = models.CharField(max_length=255)
    agency_timezone = models.CharField(max_length=50)
    agency_lang = models.CharField(max_length=10)
    agency_email = models.CharField(max_length=100)

class Route(models.Model):
    route_id = models.CharField(max_length=10)
    route_short_name = models.CharField(max_length=100)
    route_long_name = models.CharField(max_length = 100)
    route_desc = models.CharField(max_length = 100)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    route_type = models.IntegerField()
    route_color = models.CharField(max_length=10)
    route_text_color = models.CharField(max_length=10)
    route_url = models.CharField(max_length=100)

"""These draw the routes onto the map"""
class Shape(models.Model):
    shape_id = models.IntegerField()
    shape_pt_lat = models.FloatField()
    shape_pt_lon = models.FloatField()
    shape_pt_sequence = models.IntegerField()

class Fare(models.Model):
    fare_id = models.CharField(max_length=25)
    origin_id = models.CharField(max_length=10)
    destination_id = models.CharField(max_length=10)

class Fare_Attributes(models.Model):
    fare = models.ForeignKey(Fare, on_delete=models.CASCADE)
    price = models.FloatField()
    currency_type = models.CharField(max_length=10)
    payment_method = models.IntegerField()
    transfers = models.IntegerField()
    transfer_duration = models.CharField(max_length=2) # because septa xfer durations are empty

class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE) 
    service_id = models.CharField(max_length=25)
    trip_id = models.CharField(max_length=25)
    trip_headsign = models.CharField(max_length=50) 
    block_id = models.IntegerField()
    trip_short_name = models.IntegerField()
    shape = models.ForeignKey(Shape, on_delete=models.CASCADE)
    direction_id = models.IntegerField()

class Stop_Time(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    stop_sequence = models.IntegerField()
    pickup_type = models.IntegerField()
    drop_off_type = models.IntegerField()

