# testapi/urls.py
from django.urls import path
from .views import Camera1DataView, Camera2DataView, EventListView ,  user_login , user_logout 

urlpatterns = [
    path('api/camera1/upload/', Camera1DataView.as_view(), name='camera1-upload'),
    path('api/camera2/upload/', Camera2DataView.as_view(), name='camera2-upload'),
    path('api/events/', EventListView.as_view(), name='event-list'),
    # path("login/", user_login, name="login"),
    # path("logout/", user_logout, name="logout"),
]
