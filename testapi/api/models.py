from django.db import models
import uuid

class VehicleEvent(models.Model):
    event_id = models.CharField(max_length=36, default=uuid.uuid4, unique=True)
    truck_number = models.CharField(max_length=50, blank=True, null=True)
    trailer_number = models.CharField(max_length=50, blank=True, null=True)
    vehicle_type = models.CharField(max_length=50)
    camera1_image = models.TextField(blank=True, null=True)
    camera2_image = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)  # General event timestamp (last updated)
    truck_timestamp = models.DateTimeField(blank=True, null=True)  # Time when truck data was inserted
    trailer_timestamp = models.DateTimeField(blank=True, null=True)  # Time when trailer data was inserted

    def __str__(self):
        return f"Event {self.event_id} - Truck: {self.truck_number}, Trailer: {self.trailer_number}"