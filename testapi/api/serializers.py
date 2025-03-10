from rest_framework import serializers
from .models import VehicleEvent

class VehicleEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleEvent
        fields = [
            'event_id', 'truck_number', 'trailer_number', 'vehicle_type',
            'camera1_image', 'camera2_image', 'timestamp',
            'truck_timestamp', 'trailer_timestamp'  # Include the new fields
        ]