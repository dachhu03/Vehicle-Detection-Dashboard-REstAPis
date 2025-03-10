from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VehicleEvent
from .serializers import VehicleEventSerializer
import uuid
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q  # Added for OR condition in filtering

def user_login(request):
    if request.user.is_authenticated:  # Redirect if already logged in
        return redirect("dashboard")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

class Camera1DataView(APIView):
    def get(self, request, format=None):
        event_id = request.query_params.get('event_id', None)
        if event_id:
            try:
                event = VehicleEvent.objects.get(event_id=event_id)
                serializer = VehicleEventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except VehicleEvent.DoesNotExist:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            events = VehicleEvent.objects.all()
            serializer = VehicleEventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            data = request.data
            event_id = data.get('event_id', str(uuid.uuid4()))
            event, created = VehicleEvent.objects.get_or_create(
                event_id=event_id,
                defaults={
                    'truck_number': data['truck_number'],
                    'vehicle_type': data['vehicle_type'],
                    'camera1_image': data['image_data'],
                    'truck_timestamp': timezone.now()  # Set truck_timestamp when truck data is inserted
                }
            )
            if not created:
                event.camera1_image = data['image_data']
                event.truck_number = data['truck_number']
                event.truck_timestamp = timezone.now()  # Update truck_timestamp on update
                event.save()
            serializer = VehicleEventSerializer(event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Camera2DataView(APIView):
    def get(self, request, format=None):
        event_id = request.query_params.get('event_id', None)
        if event_id:
            try:
                event = VehicleEvent.objects.get(event_id=event_id)
                serializer = VehicleEventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except VehicleEvent.DoesNotExist:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            events = VehicleEvent.objects.all()
            serializer = VehicleEventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            data = request.data
            event_id = data.get('event_id', str(uuid.uuid4()))
            event, created = VehicleEvent.objects.get_or_create(
                event_id=event_id,
                defaults={
                    'trailer_number': data['trailer_number'],
                    'vehicle_type': data['vehicle_type'],
                    'camera2_image': data['image_data'],
                    'trailer_timestamp': timezone.now()  # Set trailer_timestamp when trailer data is inserted
                }
            )
            if not created:
                event.camera2_image = data['image_data']
                event.trailer_number = data['trailer_number']
                event.trailer_timestamp = timezone.now()  # Update trailer_timestamp on update
                event.save()
            serializer = VehicleEventSerializer(event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EventListView(APIView):
    def get(self, request):
        event_id = request.query_params.get('event_id', None)
        truck_number = request.query_params.get('truck_number', '')
        trailer_number = request.query_params.get('trailer_number', '')
        search = request.query_params.get('search', '')  # Added search parameter
        date = request.query_params.get('date', '')
        vehicle_type = request.query_params.get('vehicle_type', '')
        from_date = request.query_params.get('from_date', '')
        to_date = request.query_params.get('to_date', '')

        events = VehicleEvent.objects.all()

        # Apply filters
        if event_id:
            events = events.filter(event_id=event_id)
        if truck_number:
            events = events.filter(truck_number__icontains=truck_number)
        if trailer_number:
            events = events.filter(trailer_number__icontains=trailer_number)
        if search:  # Handle search parameter
            events = events.filter(
                Q(truck_number__icontains=search) | Q(trailer_number__icontains=search)
            )
        if date:
            events = events.filter(timestamp__date=date)
        if vehicle_type:
            events = events.filter(vehicle_type__icontains=vehicle_type)
        if from_date and to_date:
            try:
                from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
                events = events.filter(timestamp__date__gte=from_date_obj, timestamp__date__lte=to_date_obj)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif from_date or to_date:
            return Response(
                {"error": "Both 'from_date' and 'to_date' parameters are required for date range filtering."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = VehicleEventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            data = request.data
            event_id = data.get('event_id', str(uuid.uuid4()))
            event = VehicleEvent.objects.create(
                event_id=event_id,
                truck_number=data.get('truck_number', ''),
                trailer_number=data.get('trailer_number', ''),
                vehicle_type=data['vehicle_type'],
                camera1_image=data.get('camera1_image', ''),
                camera2_image=data.get('camera2_image', ''),
                truck_timestamp=timezone.now() if data.get('truck_number') else None,
                trailer_timestamp=timezone.now() if data.get('trailer_number') else None
            )
            serializer = VehicleEventSerializer(event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"error": f"Missing required field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)