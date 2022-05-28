from django.urls import path
from map import views

urlpatterns = [
    path('business/', views.BusinessDetails.as_view(), name=''),
    path('user-create/', views.UserView.as_view(), name=''),
]