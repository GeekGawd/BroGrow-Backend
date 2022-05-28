from django.urls import path
from map.views import BusinessDetails

urlpatterns = [
    path('business/', BusinessDetails.as_view(), name=''),
]