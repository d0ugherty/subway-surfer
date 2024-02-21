from django.db import models
from collections import defaultdict
import json

class Stop(models.Model):
    stop_id = models.IntegerField()
    stop_name = models.CharField(max_length=100)
    stop_desc = models.CharField(max_length=100)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    zone_id = models.CharField(max_length=10)
    stop_url = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.stop_name

    @classmethod
    def get_stop(cls, stop_name):
        try:
            return cls.objects.get(stop_name=stop_name)
        except cls.DoesNotExist:
            return None
    
    def lat_lon(self):
        lat = self.stop_lat
        lon = self.stop_lon
        return [lat, lon]
    
    def get_stop_times(self):
        return Stop_Time.objects.filter(stop_id=self.stop_id).select_related("stop")
    
class Agency(models.Model):
    agency_id = models.CharField(max_length=25)
    agency_name = models.CharField(max_length=50)
    agency_url = models.CharField(max_length=255)
    agency_timezone = models.CharField(max_length=50)
    agency_lang = models.CharField(max_length=10)
    agency_email = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.agency_name
    
    @classmethod
    def get_agency(cls, agency_id):
        try:
            return cls.objects.get(agency_id=agency_id)
        except cls.DoesNotExist:
            return None
        
    def get_routes(self):
        return Route.objects.filter(agency=self).select_related('agency')
    
    def get_stops(self):
        return Stop.objects.filter(stop_time__trip__route__agency_id=self.id).distinct()
    
    """ 
    Queries for retrieving the shape data. Shape data doesn't have a route 
    or agency associated with it so you have to bridge through trips. 
    Makes sense when you think about.
    """
    def get_shapes(self, serialize=True):
        agency_route_trips = Trip.objects.filter(route__agency=self).values_list('shape_id', flat=True).distinct()
        agency_shapes = Shape.objects.filter(shape_id__in=agency_route_trips).values_list("shape_id", "shape_pt_lon", "shape_pt_lat")
        # Serialize to use it into a JSON string to use it with JavaScript
        # this is faster than using the built-in serializer
        if serialize:
            shape_dict = defaultdict(list)
            for row in agency_shapes:
                shape_id, shape_pt_lon, shape_pt_lat = row
                shape_dict[shape_id].append({'shape_pt_lat': shape_pt_lat, 'shape_pt_lon': shape_pt_lon})
            agency_shapes = json.dumps(shape_dict)
        return agency_shapes

class Route(models.Model):
    route_id = models.CharField(max_length=10)
    route_short_name = models.CharField(max_length=100)
    route_long_name = models.CharField(max_length = 100)
    route_desc = models.CharField(max_length = 100, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    route_type = models.IntegerField()
    route_color = models.CharField(max_length=10, null=True)
    route_text_color = models.CharField(max_length=10, null=True)
    route_url = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.route_long_name)
    
"""These draw the routes onto the map"""
class Shape(models.Model):
    shape_id = models.IntegerField()
    shape_pt_lat = models.FloatField()
    shape_pt_lon = models.FloatField()
    shape_pt_sequence = models.IntegerField()
    shape_dist_traveled = models.FloatField(null=True)

    def lat_lon(self):
        return [self.shape_pt_lat, self.shape_pt_lon]

class Fare(models.Model):
    fare_id = models.CharField(max_length=25)
    origin_id = models.CharField(max_length=10)
    destination_id = models.CharField(max_length=10)

    @classmethod
    def get_fare_obj(cls, origin_id, destination_id):
        try:
            return cls.objects.get(origin_id=origin_id, destination_id=destination_id)
        except cls.DoesNotExist:
            return None
        
    def price(self):
        fare_price = Fare_Attributes.objects.get(fare=self).price
        return fare_price

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
    block_id = models.CharField(max_length=10)
    trip_short_name = models.IntegerField(null=True)
    shape_id= models.IntegerField()
    direction_id = models.IntegerField()

    @classmethod
    def get_trip(cls,train_id):
        try:
            return cls.objects.filter(block_id=train_id).latest('block_id')
        except cls.DoesNotExist:
            return None
    
    def route_name(self):
        return self.route.route_short_name
        

class Stop_Time(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    stop_sequence = models.IntegerField()
    pickup_type = models.IntegerField(null=True)
    drop_off_type = models.IntegerField(null=True)

class Calendar_Date(models.Model):
    service_id = models.CharField(max_length=25)
    date = models.CharField(max_length=25)
    exception_type = models.IntegerField()

class Calendar(models.Model):
    service_id = models.CharField(max_length=25)
    monday = models.IntegerField()
    tuesday = models.IntegerField()
    wednesday = models.IntegerField()
    thursday = models.IntegerField()
    friday = models.IntegerField()
    saturday = models.IntegerField()
    sunday = models.IntegerField()
    start_date = models.CharField(max_length=25)
    end_date = models.CharField(max_length=25)